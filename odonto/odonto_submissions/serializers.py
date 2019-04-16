import datetime
from collections import OrderedDict
from fp17.bcds1 import Patient, Treatment
from odonto import models
from django.db import models as django_models
from fp17 import treatments as t
from fp17 import exemptions as e
from fp17.envelope import Envelope
from fp17.bcds1 import BCDS1, Patient as FP17_Patient


class TreatmentSerializer(object):
    message = Treatment
    TREATMENT_MAPPINGS = None

    def __init__(self, model_instance):
        self.model_instance = model_instance

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

    TREATMENT_MAPPINGS = OrderedDict([
        ("urgent_treatment", t.TREATMENT_CATEGORY_URGENT),
        ("regulation_11_replacement_appliance", t.REGULATION_11_APPLIANCE),
        ("prescription_only", t.PRESCRIPTION),
        ("denture_repairs", t.DENTURE_REPAIRS),
        ("bridge_repairs", t.BRIDGE_REPAIRS),
        ("arrest_of_bleeding", t.ARREST_OF_BLEEDING),
        ("removal_of_sutures", t.REMOVAL_OF_SUTURES)
    ])

    def to_messages(self):
        messages = super().to_messages()
        category = ["Band 1", "Band 2", "Band 3"]
        if self.model_instance.treatment_category:
            # urgent treatments do not have a treatment category
            band_number = category.index(
                self.model_instance.treatment_category
            )
            band_number = band_number + 1
            messages.insert(
                0, t.TREATMENT_CATEGORY(band_number)
            )
        return messages


class Fp17ClinicalDataSetSerializer(TreatmentSerializer):
    model = models.Fp17ClinicalDataSet

    TREATMENT_MAPPINGS = OrderedDict([
        ("examination", t.EXAMINATION),
        ("scale_and_polish", t.SCALE_AND_POLISH),
        ("fluoride_varnish", t.FLUORIDE_VARNISH),
        ("fissure_sealants", t.FISSURE_SEALANTS),
        ("radiographs_taken", t.RADIOGRAPHS),
        ("endodontic_treatment", t.ENDODONTIC_TREATMENT),
        (
            "permanent_fillings_and_sealant_restorations",
            t.PERMANENT_FILLINGS_AND_SEALANT_RESTORATIONS
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
            t.REFERRAL_FOR_ADVANCED_MANDATORY_SERVICES
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
    ])


class Fp17RecallSerializer(TreatmentSerializer):
    model = models.Fp17Recall

    TREATMENT_MAPPINGS = {
        "number_of_months": t.RECALL_INTERVAL
    }


class Fp17OtherDentalServiceTranslator(TreatmentSerializer):
    model = models.Fp17OtherDentalServices

    TREATMENT_MAPPINGS = {
        # "treatment_on_referral":  #TODO this is not mapped
        "free_repair_or_replacement": t.FREE_REPAIR_REPLACEMENT,
        "further_treatment_within_2_months":
            t.FURTHER_TREATMENT_WITHIN_TWO_MONTHS,
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
        "income_related_employment_and_support_allowance":
            e.INCOME_RELATED_EMPLOYMENT_AND_SUPPORT_ALLOWANCE,
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


class DemographicsTranslater(object):
    def __init__(self, model_instance):
        self.model_instance = model_instance

    ETHNICITY_MAPPINGS = {
        "White british": t.ETHNIC_ORIGIN_1_WHITE_BRITISH,
        "White irish": t.ETHNIC_ORIGIN_2_WHITE_IRISH,
        "White other": t.ETHNIC_ORIGIN_3_WHITE_OTHER,
        "White and black caribbean":
            t.ETHNIC_ORIGIN_4_WHITE_AND_BLACK_CARIBBEAN,
        "White and black african": t.ETHNIC_ORIGIN_5_WHITE_AND_BLACK_AFRICAN,
        "White and asian": t.ETHNIC_ORIGIN_6_WHITE_AND_ASIAN,
        "Other mixed background": t.ETHNIC_ORIGIN_7_OTHER_MIXED_BACKGROUND,
        "Asian or asian british indian":
            t.ETHNIC_ORIGIN_8_ASIAN_OR_ASIAN_BRITISH_INDIAN,
        "Asian or asian british pakistani":
            t.ETHNIC_ORIGIN_9_ASIAN_OR_ASIAN_BRITISH_PAKISTANI,
        "Asian or asian british bangladeshi":
            t.ETHNIC_ORIGIN_10_ASIAN_OR_ASIAN_BRITISH_BANGLADESHI,
        "Other asian background": t.ETHNIC_ORIGIN_11_OTHER_ASIAN_BACKGROUND,
        "Black or black british caribbean":
            t.ETHNIC_ORIGIN_12_BLACK_OR_BLACK_BRITISH_CARIBBEAN,
        "Black or black british african":
            t.ETHNIC_ORIGIN_13_BLACK_OR_BLACK_BRITISH_AFRICAN,
        "Other black background": t.ETHNIC_ORIGIN_14_OTHER_BLACK_BACKGROUND,
        "Chinese": t.ETHNIC_ORIGIN_15_CHINESE,
        "Other ethnic group": t.ETHNIC_ORIGIN_ANY_OTHER_ETHNIC_GROUP,
        "Patient declined": t.ETHNIC_ORIGIN_PATIENT_DECLINED
    }

    def sex(self):
        if self.model_instance.sex == "Female":
            return "F"
        elif self.model_instance.sex == "Male":
            return "M"

        raise ValueError(
            "The form requires a sex of either 'Female' or 'Male'"
        )

    def ethnicity(self):
        return self.ETHNICITY_MAPPINGS.get(self.model_instance.ethnicity)

    def address(self):
        result = [
            "{} {}".format(
                self.model_instance.house_number_or_name,
                self.model_instance.street
            )
        ]
        if self.model_instance.city_or_town:
            result.append(self.model_instance.city_or_town)

        if self.model_instance.county:
            result.append(self.model_instance.county)
        return result


def get_envelope(episode, user):
    """
    Gets the envelope information
    TODO currently needs:

    - site number/origin
    Mandatory.
    Corresponds to Interchange to which this segment refers.

    - destination
    For messages orginated by the system, the unique
    five digit site number issued by the service.  Messages
    originated by a user use the code appropriate to the service.

    - approval_number
    The practice system approval number is the supplier number provided
    by the NHSDS.

    - serial_number
    sequential serial number of the interchange that was sent (optional)
    """
    envelope = Envelope()
    envelope.release_timestamp = datetime.datetime.utcnow()
    return envelope


def get_bcds1(episode, user):
    """
    Gets the envelope information
    TODO current needs
    - message_reference_number
    Sequential number assigned by the practice application that within
    contract number (9105) uniquely identifies a message.

    - contract number
    For message types BCDS1
    Provider’s unique 10 digit contract number:

    - pin
    The practice system must ensure that once a dentist has entered the DPB
    PIN to authorise a batch of claims prior to transmission that no further
    claims may be added in his/her name.
    """

    bcds1 = BCDS1()
    provider = episode.patient.fp17dentalcareprovider.get()
    bcds1.location = provider.provider_location_number
    performer_number = user.performernumber.first()

    if not performer_number:
        raise ValueError(
            "No performer number for user {}".format(user.id)
        )

    bcds1.performer_number = performer_number.number
    bcds1.patient = FP17_Patient()


def translate_episode_to_xml(episode, user):
    bcds1 = get_bcds1(episode, user)
    envelope = get_envelope(episode, user)
    envelope.add_message(bcds1)
    assert not bcds1.get_errors(), bcds1.get_errors()
    assert not envelope.get_errors(), envelope.get_errors()
    root = envelope.generate_xml()
    Envelope.validate_xml(root)
    return root


def translate_to_bdcs1(bcds1, episode):
    demographics = episode.patient.demographics()
    demographics_translater = DemographicsTranslater(demographics)
    bcds1.patient.surname = demographics.surname
    bcds1.patient.forename = demographics.first_name
    bcds1.patient.date_of_birth = demographics.date_of_birth
    bcds1.patient.address = demographics_translater.address()
    bcds1.patient.sex = demographics_translater.sex()

    incomplete_treatment = episode.fp17incompletetreatment_set.get()
    bcds1.date_of_acceptance = incomplete_treatment.date_of_acceptance
    bcds1.date_of_completion = incomplete_treatment.completion_or_last_visit
    bcds1.treatments = []

    translators = [
        Fp17TreatmentCategorySerializer,
        Fp17ClinicalDataSetSerializer,
        Fp17RecallSerializer,
        Fp17OtherDentalServiceTranslator
    ]

    for translator in translators:
        model = translator.model
        qs = model.objects.filter(episode=episode)
        for instance in qs:
            bcds1.treatments.extend(
                translator(instance).to_messages()
            )

    ethnicity_treatment = demographics_translater.ethnicity()

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
