import datetime
from collections import OrderedDict
from lxml import etree
from fp17.bcds1 import Treatment
from django.conf import settings
from odonto import models
from odonto import episode_categories
from opal.core import subrecords
from django.db import models as django_models
from fp17 import treatments as t
from fp17 import exemptions as e
from fp17.envelope import Envelope
from fp17.bcds1 import BCDS1, Patient as FP17_Patient


class SerializerValidationError(Exception):
    pass


class TreatmentSerializer(object):
    message = Treatment
    TREATMENT_MAPPINGS = None

    def __init__(self, episode):
        self.episode = episode
        self.patient = episode.patient

        model_attribute_name = f"{self.model.__name__}_set".lower()

        if self.model in subrecords.patient_subrecords():
            parent = self.patient
        else:
            parent = self.episode
        self.model_instance = getattr(parent, model_attribute_name).get()

    def get_field(self, name):
        return self.model_instance._meta.get_field(name)

    def is_integer(self, name):
        field = self.get_field(name)
        return isinstance(field, django_models.IntegerField)

    def to_messages(self):
        """
        Translates fields to messages.

        If the field is an integer it expects a treatment class
        that takes the integer.

        Otherwise it assumes that you should add the treatment
        if the field on the class is truthy.
        """
        treatments = []

        for k, v in self.TREATMENT_MAPPINGS.items():
            value = getattr(self.model_instance, k)
            if self.is_integer(k):
                if value is not None:
                    treatments.append(v(value))
            elif value:
                treatments.append(v)
        return treatments


class Fp17TreatmentCategorySerializer(TreatmentSerializer):
    model = models.Fp17TreatmentCategory

    TREATMENT_MAPPINGS = OrderedDict(
        [
            ("urgent_treatment", t.TREATMENT_CATEGORY_URGENT),
            ("regulation_11_replacement_appliance", t.REGULATION_11_APPLIANCE),
            ("prescription_only", t.PRESCRIPTION),
            ("denture_repairs", t.DENTURE_REPAIRS),
            ("bridge_repairs", t.BRIDGE_REPAIRS),
            ("arrest_of_bleeding", t.ARREST_OF_BLEEDING),
            ("removal_of_sutures", t.REMOVAL_OF_SUTURES),
        ]
    )

    def to_messages(self):
        messages = super().to_messages()
        category = ["Band 1", "Band 2", "Band 3"]
        if self.model_instance.treatment_category:
            # urgent treatments do not have a treatment category
            band_number = category.index(self.model_instance.treatment_category)
            band_number = band_number + 1
            messages.insert(0, t.TREATMENT_CATEGORY(band_number))
        return messages


class Fp17ClinicalDataSetSerializer(TreatmentSerializer):
    model = models.Fp17ClinicalDataSet

    TREATMENT_MAPPINGS = OrderedDict(
        [
            ("examination", t.EXAMINATION),
            ("scale_and_polish", t.SCALE_AND_POLISH),
            ("fluoride_varnish", t.FLUORIDE_VARNISH),
            ("fissure_sealants", t.FISSURE_SEALANTS),
            ("radiographs_taken", t.RADIOGRAPHS),
            ("endodontic_treatment", t.ENDODONTIC_TREATMENT),
            (
                "permanent_fillings_and_sealant_restorations",
                t.PERMANENT_FILLINGS_AND_SEALANT_RESTORATIONS,
            ),
            ("extractions", t.EXTRACTION),
            ("crowns_provided", t.CROWN),
            ("upper_denture_acrylic", t.UPPER_DENTURE_ACRYLIC),
            ("lower_denture_acrylic", t.LOWER_DENTURE_ACRYLIC),
            ("upper_denture_metal", t.UPPER_DENTURE_METAL),
            ("lower_denture_metal", t.LOWER_DENTURE_METAL),
            ("veneers_applied", t.VENEERS_APPLIED),
            ("inlays", t.INLAYS),
            ("bridges_fitted", t.BRIDGES_FITTED),
            (
                "referral_for_advanced_mandatory_services_band",
                t.REFERRAL_FOR_ADVANCED_MANDATORY_SERVICES,
            ),
            ("antibiotic_items_prescribed", t.ANTIBIOTIC_ITEMS),
            ("other_treatment", t.OTHER_TREATMENT),
            ("best_practice_prevention", t.BEST_PRACTICE_PREVENTION),
            ("decayed_teeth_permanent", t.DECAYED_PERMANENT),
            ("decayed_teeth_deciduous", t.DECAYED_DECIDUOUS),
            ("missing_teeth_permanent", t.MISSING_PERMANENT),
            ("missing_teeth_deciduous", t.MISSING_DECIDUOUS),
            ("filled_teeth_permanent", t.FILLED_PERMANENT),
            ("filled_teeth_deciduous", t.FILLED_TEETH_DECIDUOUS),
        ]
    )


class Fp17RecallSerializer(TreatmentSerializer):
    model = models.Fp17Recall

    TREATMENT_MAPPINGS = {"number_of_months": t.RECALL_INTERVAL}


class Fp17OtherDentalServiceTranslator(TreatmentSerializer):
    model = models.Fp17OtherDentalServices

    TREATMENT_MAPPINGS = {
        # "treatment_on_referral":  #TODO this is not mapped
        "free_repair_or_replacement": t.FREE_REPAIR_REPLACEMENT,
        "further_treatment_within_2_months": t.FURTHER_TREATMENT_WITHIN_TWO_MONTHS,
        "domicillary_services": t.DOMICILIARY_SERVICES,
        "sedation_services": t.SEDATION_SERVICES,
    }


class ExceptionSerializer(object):
    EXEMPTION_MAPPINGS = {
        "patient_under_18": e.PATIENT_UNDER_18,
        "full_remission_hc2_cert": e.FULL_REMISSION,
        "partial_remission_hc3_cert": e.PARTIAL_REMISSION,
        "expectant_mother": e.EXPECTANT_MOTHER,
        "nursing_mother": e.NURSING_MOTHER,
        "aged_18_in_full_time_education": e.AGED_18_IN_FULL_TIME_EDUCATION,
        "income_support": e.INCOME_SUPPORT,
        # "nhs_tax_credit_exemption" TODO this does not exist
        "income_based_jobseekers_allowance": e.JOBSEEKERS_ALLOWANCE,
        "pension_credit_guarantee_credit": e.PENSION_CREDIT_GUARANTEE_CREDIT,
        "prisoner": e.PRISONER,
        "universal_credit": e.UNIVERSAL_CREDIT,
        "income_related_employment_and_support_allowance": e.INCOME_RELATED_EMPLOYMENT_AND_SUPPORT_ALLOWANCE,
        # "patient_charge_collected" TODO this is not exist
    }

    def __init__(self, model_instance):
        self.model_instance = model_instance

    def exemptions(self):
        result = {}
        for i, v in self.EXEMPTION_MAPPINGS.items():
            if getattr(self.model_instance, i):
                # Prisoner does not have a concept of no exemption seen
                if i == "prisoner":
                    result["code"] = v
                    continue

                if self.model_instance.evidence_of_exception_or_remission_seen:
                    result["code"] = v.EVIDENCE_SEEN
                else:
                    result["code"] = v.NO_EVIDENCE_SEEN

        return result

    def charge(self):
        if self.model_instance.patient_charge_collected:
            return int(self.model_instance.patient_charge_collected * 100)


class OrthodonticDataSetTranslator(TreatmentSerializer):
    model = models.OrthodonticDataSet

    TREATMENT_MAPPINGS = {
        "radiograph": t.RADIOGRAPHS,
        "removable_upper_appliance": t.REMOVABLE_UPPER_APPLIANCE,
        "removable_lower_appliance": t.REMOVABLE_LOWER_APPLIANCE,
        "fixed_upper_appliance": t.FIXED_UPPER_APPLIANCE,
        "fixed_lower_appliance": t.FIXED_LOWER_APPLIANCE,
        "function_appliance": t.FUNCTIONAL_APPLIANCE,
        "retainer_upper": t.RETAINER_UPPER,
        "retainer_lower": t.RETAINER_LOWER,
    }


class ExtractionChartTranslator(TreatmentSerializer):
    model = models.ExtractionChart

    def get_teeth_field_to_code_mapping(self):
        """
        1st digit – quadrant clockwise from upper right 1-4 for
        permanent teeth and 5-8 for deciduous teeth
        2nd digit – tooth in quadrant counting out from midline 1-8
        for permanent teeth, 1-5 for deciduous teeth.
        Supernumerary teeth identified as 9
        """
        quadrents = ["ur", "lr", "ll", "ul"]
        permanent_teeth = list(range(1, 9))
        deciduous_teeth = ["a", "b", "c", "d", "e"]
        teeth = permanent_teeth + deciduous_teeth
        teeth_fields_to_code = {}

        for quadrant_idx, quadrant in enumerate(quadrents):
            for tooth in teeth:
                tooth_field = f"{quadrant}_{tooth}"
                if tooth in deciduous_teeth:
                    quadrant_code = quadrant_idx + 5
                    tooth_code = deciduous_teeth.index(tooth) + 1
                else:
                    quadrant_code = quadrant_idx + 1
                    tooth_code = tooth
                code = int(f"{quadrant_code}{tooth_code}")
                teeth_fields_to_code[tooth_field] = code

        return teeth_fields_to_code

    def to_messages(self):
        teeth_fields_to_code = self.get_teeth_field_to_code_mapping()
        result = []
        for field, code in teeth_fields_to_code.items():
            if getattr(self.model_instance, field):
                result.append(t.ORTHODONTIC_EXTRACTIONS(code))
        return result


class OrthodonticAssessmentTranslator(TreatmentSerializer):
    model = models.OrthodonticAssessment

    TREATMENT_MAPPINGS = {

        "aesthetic_component": t.AESTHETIC_COMPONENT,
        "iotn": t.IOTN,
    }

    def validate(self):
        today = datetime.date.today()
        date_fitted = self.model_instance.date_of_appliance_fitted
        date_of_assessment = self.model_instance.date_of_assessment
        date_of_referral = self.model_instance.date_of_referral

        # date of referral checks
        if date_of_referral:
            if date_of_referral > today:
                raise SerializerValidationError(
                    "Date of referral must not be in the future"
                )

            if not self.model_instance.assessment:
                raise SerializerValidationError(
                    "An assessment is required if there is a date of referral"
                )

            if date_of_assessment and date_of_referral > date_of_assessment:
                raise SerializerValidationError(
                    "Date of assessment must be greater than the date of referral"
                )

        if date_of_assessment and date_of_assessment >= datetime.date(2019, 4, 1):
            if not date_of_referral:
                raise SerializerValidationError(
                    "Date of referral is required if there is a date of assessment"
                )

        # date of assessment checks
        if date_of_assessment and date_of_assessment > today:
            raise SerializerValidationError(
                "Date of assessment must not be in the future"
            )

        if self.model_instance.assessment:
            if not date_of_assessment:
                raise SerializerValidationError(
                    'Date of assessment is required if "Assess and review", \
"Assess and refuse treatment" or "Assess and appliance fitted" are populated'
                )

        # date of appliance fitted checks
        if date_fitted and date_of_assessment:
            if date_fitted < date_of_assessment:
                raise SerializerValidationError(
                    "Date appliance fitted prior to date of assessment"
                )

        if self.model_instance.assessment == self.model_instance.ASSESS_AND_APPLIANCE_FITTED:
            if not date_fitted:
                raise SerializerValidationError(
                    'Date of appliance fitted is required if "Assess and \
appliance fitted"'
                )

    def to_messages(self):
        self.validate()
        result = super().to_messages()

        if self.model_instance.iotn_not_applicable:
            # If ‘IOTN not applicable’ (e.g not possible to calculate
            # because the patient has transferred mid treatment to a new
            # Provider contract)
            # a value of 0 (zero) should be entered
            result.append(t.IOTN(0))

        if self.model_instance.assessment == self.model_instance.ASSESSMENT_AND_REVIEW:
            result.append(t.ASSESS_AND_REVIEW)

        if self.model_instance.assessment == self.model_instance.ASSESS_AND_REFUSE_TREATMENT:
            result.append(t.ASSESS_AND_REFUSE)

        if self.model_instance.assessment == self.model_instance.ASSESS_AND_APPLIANCE_FITTED:
            result.append(t.ASSESS_AND_APPLIANCE_FITTED)

        if self.model_instance.date_of_referral:
            dt = self.model_instance.date_of_referral
            result.append(t.DAY_OF_REFERRAL(dt.day))
            result.append(t.MONTH_OF_REFERRAL(dt.month))
            result.append(t.YEAR_OF_REFERRAL(int(str(dt.year)[2:])))

        if self.model_instance.date_of_appliance_fitted:
            dt = self.model_instance.date_of_appliance_fitted
            result.append(t.DAY_APPLIANCE_FITTED(dt.day))
            result.append(t.MONTH_APPLIANCE_FITTED(dt.month))
            result.append(t.YEAR_APPLIANCE_FITTED(int(str(dt.year)[2:])))

        return result


class OrthodonticTreatmentTranslator(TreatmentSerializer):
    model = models.OrthodonticTreatment

    TREATMENT_MAPPINGS = {
        "aesthetic_component": t.AESTHETIC_COMPONENT,
        "iotn": t.IOTN,
        "repair": t.REPAIR_TO_APPLIANCE_FITTED_BY_ANOTHER_DENTIST,
        "replacement": t.REGULATION_11_REPLACEMENT_APPLIANCE,
        "treatment_discontinued": t.TREATMENT_DISCONTINUED,
        "treatment_completed": t.TREATMENT_COMPLETED,
        "par_scores_calculated": t.PAR_SCORES_CALCULATED,
    }

    def to_messages(self):
        result = super().to_messages()

        if self.model_instance.iotn_not_applicable:
            # If ‘IOTN not applicable’ (e.g not possible to calculate
            # because the patient has transferred mid treatment to a new
            # Provider contract)
            # a value of 0 (zero) should be entered
            result.append(t.IOTN(0))

        if (
            sum(
                [
                    self.model_instance.patient_failed_to_return,
                    self.model_instance.patient_requested_stop,
                    self.model_instance.treatment_discontinued,
                    self.model_instance.treatment_completed,
                ]
            )
            > 1
        ):
            raise ValueError("Inconsistent reasons for stopping an FP17O")

        if self.model_instance.patient_failed_to_return:
            result.append(t.TREATMENT_ABANDONED)
            result.append(t.PATIENT_FAILED_TO_RETURN)

        if self.model_instance.patient_requested_stop:
            result.append(t.TREATMENT_ABANDONED)
            result.append(t.PATIENT_REQUESTED)
        return result


class DemographicsTranslator(TreatmentSerializer):
    model = models.Demographics

    ETHNICITY_MAPPINGS = {
        "White british": t.ETHNIC_ORIGIN_1_WHITE_BRITISH,
        "White irish": t.ETHNIC_ORIGIN_2_WHITE_IRISH,
        "White other": t.ETHNIC_ORIGIN_3_WHITE_OTHER,
        "White and black caribbean": t.ETHNIC_ORIGIN_4_WHITE_AND_BLACK_CARIBBEAN,
        "White and black african": t.ETHNIC_ORIGIN_5_WHITE_AND_BLACK_AFRICAN,
        "White and asian": t.ETHNIC_ORIGIN_6_WHITE_AND_ASIAN,
        "Other mixed background": t.ETHNIC_ORIGIN_7_OTHER_MIXED_BACKGROUND,
        "Asian or asian british indian": t.ETHNIC_ORIGIN_8_ASIAN_OR_ASIAN_BRITISH_INDIAN,
        "Asian or asian british pakistani": t.ETHNIC_ORIGIN_9_ASIAN_OR_ASIAN_BRITISH_PAKISTANI,
        "Asian or asian british bangladeshi": t.ETHNIC_ORIGIN_10_ASIAN_OR_ASIAN_BRITISH_BANGLADESHI,
        "Other asian background": t.ETHNIC_ORIGIN_11_OTHER_ASIAN_BACKGROUND,
        "Black or black british caribbean": t.ETHNIC_ORIGIN_12_BLACK_OR_BLACK_BRITISH_CARIBBEAN,
        "Black or black british african": t.ETHNIC_ORIGIN_13_BLACK_OR_BLACK_BRITISH_AFRICAN,
        "Other black background": t.ETHNIC_ORIGIN_14_OTHER_BLACK_BACKGROUND,
        "Chinese": t.ETHNIC_ORIGIN_15_CHINESE,
        "Other ethnic group": t.ETHNIC_ORIGIN_ANY_OTHER_ETHNIC_GROUP,
        "Patient declined": t.ETHNIC_ORIGIN_PATIENT_DECLINED,
    }

    def sex(self):
        if self.model_instance.sex == "Female":
            return "F"
        elif self.model_instance.sex == "Male":
            return "M"

        raise ValueError("The form requires a sex of either 'Female' or 'Male'")

    def ethnicity(self):
        patient_ethnicity =  self.ETHNICITY_MAPPINGS.get(self.model_instance.ethnicity)
        if not patient_ethnicity:
            raise SerializerValidationError(f'Unable to find an ethnicity for patient {self.model_instance.patient_id}')
        return patient_ethnicity

    def address(self):
        address_list = [
            "{} {}".format(
                self.model_instance.house_number_or_name, self.model_instance.street
            )
        ]
        if self.model_instance.city_or_town:
            address_list.append(self.model_instance.city_or_town)

        if self.model_instance.county:
            address_list.append(self.model_instance.county)

        address_list = [i for i in address_list]

        result = []
        for address_line in address_list:
            cleaned_line = "".join(i for i in address_line if i.isalnum() or i == " ")
            result.append(cleaned_line[:32].upper())
        return result

    def forename(self):
        return clean_non_alphanumeric(self.model_instance.first_name).upper()

    def surname(self):
        return clean_non_alphanumeric(self.model_instance.surname).upper()

    def post_code(self):
        if self.model_instance.post_code:
            return clean_non_alphanumeric(self.model_instance.post_code).upper()


def get_envelope(episode, transmission_id):
    """
    Gets the envelope information
    """
    envelope = Envelope()
    care_provider = episode.fp17dentalcareprovider_set.get()
    envelope.origin = care_provider.provider_location_number
    envelope.release_timestamp = datetime.datetime.utcnow()
    envelope.serial_number = transmission_id

    envelope.origin = str(settings.DPB_SITE_ID)
    envelope.destination = settings.DESTINATION

    envelope.approval_number = 1
    envelope.release_timestamp = datetime.datetime.utcnow()
    return envelope


def get_bcds1(episode, submission_id, submission_count):
    """
    creates a a BDCS1 message segmant.

    message_id is the unique message referant
    Gets the bcs1 information
    """

    bcds1 = BCDS1()
    # According to the spec this is a required random number
    # however upscompass have requested the following numbers
    if episode.category_name == episode_categories.FP17Episode.display_name:
        bcds1.contract_number = settings.FP17_CONTRACT_NUMBER
    elif episode.category_name == episode_categories.FP17OEpisode.display_name:
        bcds1.contract_number = settings.FP17O_CONTRACT_NUMBER
    bcds1.message_reference_number = submission_id
    bcds1.resubmission_count = submission_count
    provider = episode.fp17dentalcareprovider_set.get()
    bcds1.location = settings.LOCATION
    performer = provider.get_performer_obj()

    if not performer:
        raise ValueError(
            "Unable to get the performer name {} from care provider {}".format(
                provider.performer, provider.id
            )
        )

    bcds1.performer_number = int(performer.number)
    bcds1.dpb_pin = performer.dpb_pin
    bcds1.patient = FP17_Patient()
    translate_to_bdcs1(bcds1, episode)
    return bcds1


def translate_episode_to_xml(episode, submission_id, submission_count, transmission_id):
    bcds1 = get_bcds1(episode, submission_id, submission_count)
    envelope = get_envelope(episode, transmission_id)
    envelope.add_message(bcds1)
    assert not bcds1.get_errors(), bcds1.get_errors()
    assert not envelope.get_errors(), envelope.get_errors()
    root = envelope.generate_xml()
    Envelope.validate_xml(root)
    return etree.tostring(root, encoding="unicode", pretty_print=True).strip()


def clean_non_alphanumeric(name):
    """
    The fp17 form only accepts...

    Upper case only
    No hyphens, apostrophes or embedded spaces
    """
    return "".join(c for c in name if c.isalnum())


def translate_to_bdcs1(bcds1, episode):
    if episode.category_name == episode_categories.FP17Episode.display_name:
        return translate_to_fp17(bcds1, episode)
    elif episode.category_name == episode_categories.FP17OEpisode.display_name:
        return translate_to_fp17o(bcds1, episode)
    raise ValueError(
        f"Unable to recognise episode category {episode.category_name} \
for episode {episode.id}"
    )


def get_fp17o_date_of_acceptance(episode):
    orthodontic_assessment = episode.orthodonticassessment_set.get()
    orthodontic_treatment = episode.orthodontictreatment_set.get()

    if any(
        [
            orthodontic_treatment.patient_failed_to_return,
            orthodontic_treatment.patient_requested_stop,
            orthodontic_treatment.treatment_discontinued,
            orthodontic_treatment.treatment_completed,
        ]
    ):
        # based on the documentation...
        # "A date of last visit must be present in the Date of Completion
        # which moves into the Date of Acceptance"
        return orthodontic_treatment.date_of_completion
    else:
        return orthodontic_assessment.date_of_assessment


def translate_to_fp17o(bcds1, episode):
    demographics = episode.patient.demographics()
    demographics_translator = DemographicsTranslator(demographics)
    # surname must be upper case according to the form submitting guidelines
    bcds1.patient.surname = demographics_translator.surname()
    bcds1.patient.forename = demographics_translator.forename()

    bcds1.patient.date_of_birth = demographics.date_of_birth
    bcds1.patient.address = demographics_translator.address()
    bcds1.patient.sex = demographics_translator.sex()
    post_code = demographics_translator.post_code()

    if post_code:
        bcds1.patient.postcode = post_code

    bcds1.date_of_acceptance = get_fp17o_date_of_acceptance(episode)

    orthodontic_treatment = episode.orthodontictreatment_set.get()
    if orthodontic_treatment.date_of_completion:
        bcds1.date_of_completion = orthodontic_treatment.date_of_completion

    bcds1.treatments = []

    translators = [
        OrthodonticDataSetTranslator,
        ExtractionChartTranslator,
        OrthodonticAssessmentTranslator,
        OrthodonticTreatmentTranslator,
    ]

    for translator in translators:
        bcds1.treatments.extend(translator(episode).to_messages())

    ethnicity_treatment = demographics_translator.ethnicity()

    if ethnicity_treatment:
        bcds1.treatments.append(ethnicity_treatment)

    fp17_exemption = episode.fp17exemptions_set.get()
    exemption_translator = ExceptionSerializer(fp17_exemption)
    exemptions = exemption_translator.exemptions()
    charge = exemption_translator.charge()
    if exemptions:
        bcds1.exemption_remission = exemptions
    if charge:
        bcds1.patient_charge_pence = charge
    return bcds1


def translate_to_fp17(bcds1, episode):
    demographics = episode.patient.demographics()
    demographics_translator = DemographicsTranslator(episode)
    # surname must be upper case according to the form submitting guidelines
    bcds1.patient.surname = demographics_translator.surname()
    bcds1.patient.forename = demographics_translator.forename()

    bcds1.patient.date_of_birth = demographics.date_of_birth
    bcds1.patient.address = demographics_translator.address()
    bcds1.patient.sex = demographics_translator.sex()
    post_code = demographics_translator.post_code()

    if post_code:
        bcds1.patient.postcode = post_code

    incomplete_treatment = episode.fp17incompletetreatment_set.get()
    bcds1.date_of_acceptance = incomplete_treatment.date_of_acceptance
    bcds1.date_of_completion = incomplete_treatment.completion_or_last_visit
    bcds1.treatments = []

    translators = [
        Fp17TreatmentCategorySerializer,
        Fp17ClinicalDataSetSerializer,
        Fp17RecallSerializer,
        Fp17OtherDentalServiceTranslator,
    ]

    for translator in translators:
        bcds1.treatments.extend(translator(episode).to_messages())

    ethnicity_treatment = demographics_translator.ethnicity()

    if ethnicity_treatment:
        bcds1.treatments.append(ethnicity_treatment)

    fp17_exemption = episode.fp17exemptions_set.get()
    exemption_translator = ExceptionSerializer(fp17_exemption)
    exemptions = exemption_translator.exemptions()
    charge = exemption_translator.charge()
    if exemptions:
        bcds1.exemption_remission = exemptions
    if charge:
        bcds1.patient_charge_pence = charge
    return bcds1

