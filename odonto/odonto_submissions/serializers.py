import datetime
from collections import OrderedDict
from lxml import etree
from fp17.bcds1 import Treatment
from django.conf import settings
from odonto import models
from odonto import episode_categories
from odonto import constants
from opal.core import subrecords
from django.db import models as django_models
from fp17 import treatments as t
from fp17 import exemptions as e
from fp17.envelope import Envelope
from fp17.bcds1 import (
    BCDS1,
    Patient as FP17_Patient,
    SCHEDULE_QUERY_FALSE,
    SCHEDULE_QUERY_DELETE
)


class SerializerValidationError(Exception):
    pass


def is_nhs_number_valid(nhs_number):
    """
    The NHS number is a ten digit number one digit is
    check sum this validates whether the nhs number
    is true.
    """
    if not nhs_number:
        return False
    nhs_number = nhs_number.replace(" ", "")
    if not nhs_number.isnumeric():
        return False
        return "0" * 10
    if not len(nhs_number) == 10:
        return False
    # https://www.datadictionary.nhs.uk/attributes/nhs_number.html
    # step 1, for the first 9 numbers multiple by 11 - idx,
    # step 2, sum them together
    # step 3, mod the result by 11
    # step 4, if the modded result is 0, then it becomes 11
    # step 5, subtract the result from 11
    # step 6, return result == nhs_number[9]
    weighted_number = [
        int(nhs_num) * (10 - idx) for idx, nhs_num in enumerate(nhs_number[:9])
    ]
    modded = sum(weighted_number) % 11
    if modded == 0:
        modded = 11
    check_digit = 11 - modded
    return int(nhs_number[-1]) == check_digit


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

    def get_treatment_value_for_field(self, field_name, treatment):
        """
        if the model value for the field is an integer and not none return
        treatment(model_value)

        if the model value is a boolean and True return treatment
        """
        value = getattr(self.model_instance, field_name)
        if self.is_integer(field_name):
            if value is not None and not value == 0:
                return treatment(value)
        elif value:
            return treatment

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
            treatment = self.get_treatment_value_for_field(k, v)
            if treatment:
                treatments.append(treatment)
        return treatments


class Fp17CommissioningSerializer(TreatmentSerializer):
    model = models.Fp17Commissioning

    def to_messages(self):
        flexible_commissioning = self.model_instance.flexible_commissioning
        if not flexible_commissioning:
            return []
        flags = models.Fp17Commissioning.FLEXIBLE_FLAGS
        flags = [i[0] for i in flags]
        idx = flags.index(flexible_commissioning)
        return [t.FLEXIBLE_COMMISSIONING_FLAG(idx + 1)]


class Fp17IncompleteTreatmentSerializer(TreatmentSerializer):
    model = models.Fp17IncompleteTreatment

    def to_messages(self):
        incomplete_treatment = self.model_instance.incomplete_treatment
        if not incomplete_treatment:
            return []

        bands = models.Fp17IncompleteTreatment.TREATMENT_CATEGORIES
        bands = [i[0] for i in bands]
        idx = bands.index(incomplete_treatment)
        return [t.INCOMPLETE_TREATMENT(idx + 1)]


class Fp17TreatmentCategorySerializer(TreatmentSerializer):
    model = models.Fp17TreatmentCategory

    TREATMENT_MAPPINGS = OrderedDict()

    CATEGORY_TO_TREATMENT = {
        models.Fp17TreatmentCategory.BAND_1: t.TREATMENT_CATEGORY(1),
        models.Fp17TreatmentCategory.BAND_2: t.TREATMENT_CATEGORY(2),
        models.Fp17TreatmentCategory.BAND_3: t.TREATMENT_CATEGORY(3),
        models.Fp17TreatmentCategory.URGENT_TREATMENT: t.TREATMENT_CATEGORY_URGENT,
        models.Fp17TreatmentCategory.REGULATION_11_REPLACEMENT_APPLIANCE: t.REGULATION_11_APPLIANCE,
        models.Fp17TreatmentCategory.PRESCRIPTION_ONLY: t.PRESCRIPTION,
        models.Fp17TreatmentCategory.DENTURE_REPAIRS: t.DENTURE_REPAIRS,
        models.Fp17TreatmentCategory.BRIDGE_REPAIRS: t.BRIDGE_REPAIRS,
        models.Fp17TreatmentCategory.ARREST_OF_BLEEDING: t.ARREST_OF_BLEEDING,
        models.Fp17TreatmentCategory.REMOVAL_OF_SUTURES: t.REMOVAL_OF_SUTURES,
    }

    def to_messages(self):
        category = self.model_instance.treatment_category

        if category:
            if category not in self.CATEGORY_TO_TREATMENT:
                raise SerializerValidationError(f"Unknown treatment category {category}")
            return [self.CATEGORY_TO_TREATMENT[category]]
        return []


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
                "permanent_fillings",
                t.PERMANENT_FILLINGS,
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

    def to_messages(self):
        treatments = super().to_messages()
        # only include aerosols when date of acceptance is after the
        # below
        change_date = datetime.date(2020, 3, 23)
        incomplete_treatment = self.episode.fp17incompletetreatment_set.get()
        date_of_acceptance = incomplete_treatment.date_of_acceptance
        if date_of_acceptance and date_of_acceptance >= change_date:
            if self.model_instance.aerosol_generating_procedures:
                treatments.append(
                    t.AEROSOL_GENERATING_PROCEDURE(
                        self.model_instance.aerosol_generating_procedures
                    )
                )

        # Compass raises an error if it receives the below from
        # episodes with dates of acceptance prior to 1/12/21
        # before 1/12/21
        if date_of_acceptance and date_of_acceptance >= datetime.date(2021, 12, 1):
            after_1_12_21 = [
                ("pre_formed_crowns", t.PREFORMED_CROWNS),
                (
                    "advanced_perio_root_surface_debridement",
                    t.ADVANCED_PERIO_ROOT_SURFACE_DEBRIDEMENT
                ),
                ("denture_additions_reline_rebase", t.DENTURE_ADDITIONS_RELINE_REBASE),
                ("phased_treatment", t.PHASED_TREATMENT),
            ]
            for our_field, treatment_obj in after_1_12_21:
                treatment = self.get_treatment_value_for_field(
                    our_field, treatment_obj
                )
                if treatment:
                    treatments.append(treatment)
            if self.model_instance.custom_made_occlusal_appliance == self.model_instance.HARD:
                treatments.append(t.CUSTOM_MADE_OCCLUSAL_APPLIANCE_HARD_BITE)
            elif self.model_instance.custom_made_occlusal_appliance == self.model_instance.SOFT:
                treatments.append(t.CUSTOM_MADE_OCCLUSAL_APPLIANCE_SOFT_BITE)
        return treatments


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
        "aerosol_generating_procedures": t.AEROSOL_GENERATING_PROCEDURE,
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
        quadrents = ["ur", "ul",  "ll", "lr"]
        permanent_teeth = list(range(1, 10))
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
                code = f"{quadrant_code}{tooth_code}"
                teeth_fields_to_code[tooth_field] = code

        return teeth_fields_to_code

    def to_messages(self):
        teeth_fields_to_code = self.get_teeth_field_to_code_mapping()
        result = []
        teeth = []
        for field, code in teeth_fields_to_code.items():
            if getattr(self.model_instance, field):
                teeth.append(code)
        if teeth:
            result.append(t.ORTHODONTIC_EXTRACTIONS(teeth))
        return result


class OrthodonticAssessmentTranslator(TreatmentSerializer):
    model = models.OrthodonticAssessment

    TREATMENT_MAPPINGS = {
        "aesthetic_component": t.AESTHETIC_COMPONENT,
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

        if self.model_instance.iotn:
            if self.model_instance.iotn == self.model_instance.IOTN_NOT_APPLICABLE:
                # If ‘IOTN not applicable’ (e.g not possible to calculate
                # because the patient has transferred mid treatment to a new
                # Provider contract)
                # a value of 0 (zero) should be entered
                result.append(t.IOTN(0))
            else:
                result.append(t.IOTN(int(self.model_instance.iotn)))

        if self.model_instance.assessment == self.model_instance.ASSESSMENT_AND_REVIEW:
            result.append(t.ASSESS_AND_REVIEW)

        if self.model_instance.assessment == self.model_instance.ASSESS_AND_REFUSE_TREATMENT:
            result.append(t.ASSESS_AND_REFUSE)

        if self.model_instance.assessment == self.model_instance.ASSESS_AND_APPLIANCE_FITTED:
            result.append(t.ASSESS_AND_APPLIANCE_FITTED)
            # assess and appliance fitted must be accompanied by proposed treatment after 1/4/2019
            if self.model_instance.date_of_assessment and self.model_instance.date_of_assessment >= datetime.date(2019, 4, 1):
                result.append(t.PROPOSED_TREATMENT)

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
        "repair": t.REPAIR_TO_APPLIANCE_FITTED_BY_ANOTHER_DENTIST,
        "par_scores_calculated": t.PAR_SCORES_CALCULATED,
    }

    def to_messages(self):
        result = super().to_messages()

        if self.model_instance.iotn:
            if self.model_instance.iotn == self.model_instance.IOTN_NOT_APPLICABLE:
                # If ‘IOTN not applicable’ (e.g not possible to calculate
                # because the patient has transferred mid treatment to a new
                # Provider contract)
                # a value of 0 (zero) should be entered
                result.append(t.IOTN(0))
            else:
                result.append(t.IOTN(int(self.model_instance.iotn)))

        # logically it is the case you can have a replacement
        # and a conclusion but compass does not accept them.
        # Compass says in this case, just send the replacement.
        if self.model_instance.replacement:
            result.append(t.REGULATION_11_REPLACEMENT_APPLIANCE)
        elif self.model_instance.completion_type == self.model.PATIENT_FAILED_TO_RETURN:
            result.append(t.COMPLETED_TREATMENT)
            result.append(t.TREATMENT_ABANDONED)
            result.append(t.PATIENT_FAILED_TO_RETURN)
        elif self.model_instance.completion_type == self.model.PATIENT_REQUESTED:
            result.append(t.COMPLETED_TREATMENT)
            result.append(t.TREATMENT_ABANDONED)
            result.append(t.PATIENT_REQUESTED)
        elif self.model_instance.completion_type == self.model.TREATMENT_DISCONTINUED:
            result.append(t.COMPLETED_TREATMENT)
            result.append(t.TREATMENT_DISCONTINUED)
        elif self.model_instance.completion_type == self.model.TREATMENT_COMPLETED:
            result.append(t.COMPLETED_TREATMENT)
            result.append(t.TREATMENT_COMPLETED)

        return result


class CovidStatusTranslator(TreatmentSerializer):
    model = models.CovidStatus

    TREATMENT_MAPPINGS = {
        "shielding_patient": t.SHIELDING_PATIENT,
        "increased_risk": t.INCREASED_RISK,
        "possible_covid": t.POSSIBLE_COVID,
        "symptom_free": t.SYMPTOM_FREE,
        "other_covid_status": t.OTHER_COVID_STATUS,
    }


class CovidTriageTranslator(TreatmentSerializer):
    model = models.CovidTriage

    TREATMENT_MAPPINGS = {
        "dental_care_professional": t.DENTAL_CARE_PROFESSIONAL,
        "triage_via_video": t.TRIAGE_VIA_VIDEO,
        "advice_given": t.ADVICE_GIVEN,
        "advised_analgesics": t.ADVISED_ANALGESICS,
        "remote_prescription_analgesics": t.REMOTE_PRESCRIPTION_ANALGESICS,
        "remote_prescription_antibiotics": t.REMOTE_PRESCRIPTION_ANTIBIOTICS,
        "follow_up_call_required": t.FOLLOW_UP_CALL_REQUIRED,
        "call_back_if_symptoms_worsen": t.CALL_BACK_IF_SYMPTOMS_WORSEN,
        "face_to_face_appointment": t.FACE_TO_FACE_ARRANGED_BUT_NOT_ATTENDED,
    }

    def to_messages(self):
        result = super().to_messages()
        choices_fields = (
            ("referrered_to_local_udc_reason", t.REFERRERED_TO_LOCAL_UDC_REASON),
            ("covid_status", t.PATIENT_GROUP),
            ("primary_reason", t.PRIMARY_REASON),
        )
        for model_field_name, treatment in choices_fields:
            model_field = self.model._meta.get_field(model_field_name)
            choices = model_field.choices
            model_value = getattr(self.model_instance, model_field_name)
            for idx, val in enumerate(choices):
                val = val[0]
                if val == model_value:
                    result.append(treatment(idx + 1))

        hours = self.model_instance.datetime_of_contact.hour
        result.append(t.HOUR_OF_CONTACT(hours))
        minutes = self.model_instance.datetime_of_contact.minute
        result.append(t.MINUTE_OF_CONTACT(minutes))
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

    NORTH_TYNESIDE = {
        "address": [
            "PROTECTED ADDRESS",
            "CO CHILDRENS SERVICES",
            "NORTH TYNESIDE COUNCIL",
            "THE SILVERLINK NORTH",
            "COBALT BUSINESS PARK",
        ],
        "post_code": "NE27 0BY",
        "locations": [
            constants.ALBION_ROAD,
            constants.LONGBENTON,
            constants.WALLSEND,
        ]
    }

    NORTHUMBRIA = {
        "address": [
            "PROTECTED ADDRESS",
            "CO CHILDRENS SERVICES",
            "NORTHUMBERLAND COUNCIL",
            "THE OVAL",
            "STEAD LANE",
        ],
        "post_code": "NE22 5H5",
        "locations": [
            constants.AMBLE,
            constants.BLYTH,
            constants.HEXHAM,
            constants.MORPETH_NHS_CENTRE,
            constants.NORTHGATE,
            constants.SEATON_HIRST,
            constants.WARD_15_WGH
        ]
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
            raise SerializerValidationError('Unable to find an ethnicity for patient')
        return patient_ethnicity

    def phone_number(self):
        # we let people enter spaces and dashes but upstream
        # are not so forgiving
        phone_number = self.model_instance.phone_number
        if phone_number:
            return phone_number.replace(" ", "").replace("-", "")

    def get_protected_area(self):
        location = self.episode.fp17dentalcareprovider_set.get().provider_location_number
        if location in self.NORTH_TYNESIDE["locations"]:
            return self.NORTH_TYNESIDE
        if location in self.NORTHUMBRIA["locations"]:
            return self.NORTHUMBRIA
        raise ValueError(
            "Unable to find a protected address {} for episode {}".format(
                location, self.episode.id
            )
        )

    def address(self):
        if self.model_instance.protected:
            return self.get_protected_area()["address"]
        address_list = [
            "{} {}".format(
                self.model_instance.house_number_or_name, self.model_instance.street
            )
        ]
        if self.model_instance.city_or_town:
            address_list.append(self.model_instance.city_or_town)

        if self.model_instance.county:
            address_list.append(self.model_instance.county)

        result = []
        for address_line in address_list:
            cleaned_line = "".join(i for i in address_line if i.isalnum() or i == " ")
            result.append(cleaned_line[:32].upper())
        return result

    def forename(self):
        return clean_non_alphanumeric(self.model_instance.first_name).upper()

    def nhs_number(self):
        """
        Returns the nhs number of a patient if it is a number and ten digits long
        """
        # previously they did not require an NHS number, now for some forms they do
        # our users have generally been good at putting one in anyway however
        # we were not validating the field because we did not send it down as it was not
        # required.
        # now we will send it down but only if it is correctly formed and valid.
        # the client side will validate it but this was not always the case.
        #
        # the docs say that if it is not known it is still required but they
        # just expect 10 zeros
        if is_nhs_number_valid(self.model_instance.nhs_number):
            return self.model_instance.nhs_number.replace(" ", "")
        return "0" * 10

    def surname(self):
        return clean_non_alphanumeric(self.model_instance.surname).upper()

    def post_code(self):
        if self.model_instance.protected:
            return self.get_protected_area()["post_code"]

        if self.model_instance.post_code:
            return clean_non_alphanumeric(self.model_instance.post_code).upper()


def get_envelope(episode, transmission_id):
    """
    Gets the envelope information
    """
    envelope = Envelope()
    envelope.origin = settings.DPB_SITE_ID
    envelope.serial_number = transmission_id
    envelope.destination = settings.DESTINATION
    envelope.approval_number = 1
    envelope.release_timestamp = datetime.datetime.utcnow()
    return envelope


def get_bcds1(episode, submission_id, submission_count, delete=False, replace=False):
    """
    creates a a BDCS1 message segmant.

    message_id is the unique message referant
    Gets the bcs1 information
    """

    if delete and replace:
        raise ValueError(
            " ".join([
                f"Submission for {episode.id} failed,",
                "submissions can either be deleted or replaced but not both"
            ])
        )

    bcds1 = BCDS1()
    # According to the spec this is a required random number
    # however upscompass have requested the following numbers
    bcds1.message_reference_number = submission_id
    bcds1.resubmission_count = submission_count

    if delete:
        bcds1.schedule_query = SCHEDULE_QUERY_DELETE
    elif replace:
        bcds1.schedule_query = SCHEDULE_QUERY_FALSE

    provider = episode.fp17dentalcareprovider_set.get()
    bcds1.location = constants.LOCATION_NUMBERS[provider.provider_location_number]
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

    # assumption is that for a delete we do not need to do the translation
    if not delete:
        translate_to_bdcs1(bcds1, episode)
    return bcds1


def translate_episode_to_xml(
    episode,
    submission_id,
    submission_count,
    transmission_id,
    replace=False,
    delete=False
):
    bcds1 = get_bcds1(
        episode, submission_id, submission_count, delete=delete, replace=replace
    )
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
    elif episode.category_name == episode_categories.CovidTriageEpisode.display_name:
        return translate_to_covid_19(bcds1, episode)
    raise ValueError(
        f"Unable to recognise episode category {episode.category_name} \
for episode {episode.id}"
    )


def get_fp17o_date_of_acceptance(episode):
    orthodontic_assessment = episode.orthodonticassessment_set.get()
    orthodontic_treatment = episode.orthodontictreatment_set.get()

    if orthodontic_treatment.completion_type:
        # based on the documentation...
        # "A date of last visit must be present in the Date of Completion
        # which moves into the Date of Acceptance"
        result = orthodontic_treatment.date_of_completion
    else:
        result = orthodontic_assessment.date_of_assessment

    if result is None:
        raise SerializerValidationError(
            "Unable to get a date of acceptance for FP17O episode"
        )
    return result


def translate_to_fp17o(bcds1, episode):
    bcds1.contract_number = settings.FP17O_CONTRACT_NUMBER
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

    bcds1.patient.nhs_number = demographics_translator.nhs_number()

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
        CovidStatusTranslator,
    ]

    for translator in translators:
        bcds1.treatments.extend(translator(episode).to_messages())

    ethnicity_treatment = demographics_translator.ethnicity()

    if ethnicity_treatment:
        bcds1.treatments.append(ethnicity_treatment)

    if settings.ALWAYS_DECLINE_EMAIL_PHONE:
        bcds1.treatments.append(t.EMAIL_DECLINED)
        bcds1.treatments.append(t.PHONE_NUMBER_DECLINED)
    else:
        if demographics.email:
            bcds1.patient.email = demographics.email
        elif demographics.patient_declined_email:
            bcds1.treatments.append(t.EMAIL_DECLINED)
        phone_number = demographics_translator.phone_number()
        if phone_number:
            bcds1.patient.phone_number = phone_number
        elif demographics.patient_declined_phone:
            bcds1.treatments.append(t.PHONE_NUMBER_DECLINED)

    fp17_exemption = episode.fp17exemptions_set.get()
    if fp17_exemption.commissioner_approval:
        bcds1.treatments.append(t.COMMISSIONER_APPROVAL)
    exemption_translator = ExceptionSerializer(fp17_exemption)
    exemptions = exemption_translator.exemptions()
    charge = exemption_translator.charge()
    if exemptions:
        bcds1.exemption_remission = exemptions
    if charge:
        bcds1.patient_charge_pence = charge
    return bcds1


def translate_to_fp17(bcds1, episode):
    bcds1.contract_number = settings.FP17_CONTRACT_NUMBER
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

    bcds1.patient.nhs_number = demographics_translator.nhs_number()

    incomplete_treatment = episode.fp17incompletetreatment_set.get()
    bcds1.date_of_acceptance = incomplete_treatment.date_of_acceptance

    if not bcds1.date_of_acceptance:
        raise SerializerValidationError("Date of acceptance is not populated for fp17 episode")

    bcds1.date_of_completion = incomplete_treatment.completion_or_last_visit
    bcds1.treatments = []

    translators = [
        Fp17CommissioningSerializer,
        Fp17IncompleteTreatmentSerializer,
        Fp17TreatmentCategorySerializer,
        Fp17ClinicalDataSetSerializer,
        Fp17RecallSerializer,
        Fp17OtherDentalServiceTranslator,
        CovidStatusTranslator,
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


def translate_to_covid_19(bcds1, episode):
    triage = episode.covidtriage_set.get()
    if triage.triage_type == models.CovidTriage.FP17:
        bcds1.contract_number = settings.FP17_CONTRACT_NUMBER
    else:
        bcds1.contract_number = settings.FP17O_CONTRACT_NUMBER
    demographics = episode.patient.demographics()
    demographics_translator = DemographicsTranslator(episode)
    # Surname must be upper case according to the form submitting guidelines
    # Notably ethnicity should
    bcds1.patient.surname = demographics_translator.surname()
    bcds1.patient.forename = demographics_translator.forename()

    bcds1.patient.date_of_birth = demographics.date_of_birth
    bcds1.patient.address = demographics_translator.address()
    bcds1.patient.sex = demographics_translator.sex()
    bcds1.patient.nhs_number = demographics_translator.nhs_number()
    post_code = demographics_translator.post_code()

    if post_code:
        bcds1.patient.postcode = post_code

    bcds1.treatments = [t.COVID_19_TREATMENT_CATEGORY]
    bcds1.treatments.extend(CovidTriageTranslator(episode).to_messages())

    # Date of contact should be used as the acceptance and completion
    date_of_contact = episode.covidtriage_set.get().datetime_of_contact.date()
    bcds1.date_of_acceptance = date_of_contact
    bcds1.date_of_completion = date_of_contact
    return bcds1
