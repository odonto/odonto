"""
Odonto models.
"""
import datetime
from django.db.models import fields
from django.contrib.auth.models import User
from django.db import models as djangomodels

from opal import models
from opal.core.fields import enum
from odonto import constants


class Location(models.Location):
    _exclude_from_extract = True
    _advanced_searchable = False


class Allergies(models.Allergies):
    _icon = None
    pass


class Diagnosis(models.Diagnosis):
    pass


class PastMedicalHistory(models.PastMedicalHistory):
    _icon = None
    pass


class Treatment(models.Treatment):
    _icon = None

    class Meta:
        verbose_name = "Current medication"


class SymptomComplex(models.SymptomComplex):
    pass


class PatientConsultation(models.PatientConsultation):
    _icon = None

    class Meta:
        verbose_name = "Clinical notes"

    agreed_plan = fields.TextField(blank=True, default="", verbose_name="Agreed plan")
    provider_location_number = fields.CharField(
        max_length=255, blank=True, null=True,
        verbose_name="Provider location",
        choices=enum(*constants.LOCATION_NUMBERS.keys())
    )


class PerformerNumber(djangomodels.Model):
    user = djangomodels.ForeignKey(
        models.User, on_delete=djangomodels.CASCADE
    )
    number = fields.TextField(blank=True, default="")
    dpb_pin = fields.TextField(blank=True, default="")

    def __str__(self):
        return "{}: {}".format(self.user.username, self.number)


class Demographics(models.Demographics):
    _icon = None

    # patient_nhs_number = fields.IntegerField()
    # ^^^ covered by Opal Demographics.nhs_number
    # title = fields.CharField(max_length=255)  # => opal.Demographics.title
    # forenames = fields.CharField(max_length=255)  # => opal.Demographics.first_name
    # surname = fields.CharField(max_length=255)  # => opal.Demographics.surname
    # gender = fields.ChoiceField(choices=(  # => opal.Demographics.sex
    #     ('male', "Male"),
    #     ('female', "Female"),
    # ))
    # date_of_birth = fields.DateField()  # => opal.Demographics.date_of_birth

    # address apart from postcode not held in default Opal model, so it's
    # been appended to the Opal abstract model here.

    house_number_or_name = fields.CharField(
        max_length=255, null=True, blank=True,
        verbose_name="House number or name"
    )
    street = fields.CharField(max_length=255, null=True, blank=True)
    phone_number = fields.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Mobile phone number"
    )
    patient_declined_phone = fields.BooleanField(
        default=False, blank=True, verbose_name="Patient declined"
    )
    email = fields.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    patient_declined_email = fields.BooleanField(
        default=False, blank=True, verbose_name="Patient declined"
    )
    city_or_town = fields.CharField(
        max_length=255, null=True, blank=True,
        verbose_name="City or town"
    )
    county = fields.CharField(max_length=255, null=True, blank=True)
    protected = fields.BooleanField(default=False)

    def get_age(self, date=None):
        if date is None:
            date = datetime.date.today()

        if self.date_of_birth:
            born = self.date_of_birth
            return date.year - born.year - (
                (date.month, date.day) < (born.month, born.day)
            )


    # post_code = fields.CharField(max_length=255)  # => opal.Demographics.post_code
    class Meta:
        verbose_name = "Patient information"
        verbose_name_plural = "Patient information"


class CovidStatus(models.EpisodeSubrecord):
    """
    This model appears on both FP17 and FP17O forms
    and tracks the number of calls with patients of
    various covid status.

    During a course of treatment a patient can undergo
    multiple stages. E.g. they can have possible/confirmed
    covid and then later be symptom free.
    """
    _is_singleton = True

    class Meta:
        verbose_name = "COVID-19 status"
        verbose_name_plural = "COVID-19 statuses"

    shielding_patient = fields.IntegerField(
        blank=True, null=True
    )
    increased_risk = fields.IntegerField(
        blank=True,
        null=True,
        verbose_name="At increased risk"
    )
    possible_covid = fields.IntegerField(
        blank=True,
        null=True,
        verbose_name="Possible/confirmed COVID-19 or lives with a \
possible/confirmed person"
    )
    symptom_free = fields.IntegerField(
        blank=True, null=True, verbose_name="Symptom free"
    )
    other_covid_status = fields.IntegerField(
        blank=True, null=True, verbose_name="Other COVID-19 status"
    )


class Fp17DentalCareProvider(models.EpisodeSubrecord):
    _is_singleton = True

    # I'm pretty sure this should not be handled as a PatientSubrecord
    # but I'm not sure what it /should/ be
    # the following provider information is not currently in an Opal model
    # ^^^ consider splitting this into a Provider Model
    provider_location_number = fields.CharField(
        max_length=255, blank=True, null=True,
        verbose_name="Provider location",
        choices=enum(*constants.LOCATION_NUMBERS.keys())
    )
    performer = fields.CharField(
        max_length=255, blank=True, null=True
    )

    def get_performer_obj(self):
        for user in User.objects.all():
            if user.get_full_name() == self.performer:
                return user.performernumber_set.first()

    class Meta:
        verbose_name = "Performer name and clinic"


class Fp17Commissioning(models.EpisodeSubrecord):
    """
    Commissioning is something that exists in the documentation
    in the same section as the provider, however
    it only exists for FP17s and not FP17Os
    """
    _is_singleton = True

    # Note the order is important and used by the
    # serializer
    FLEXIBLE_FLAGS = enum(
        "Securing Access for Urgent Care",
        "Promoting Access to Routine Care",
        "Providing Care of High Needs Groups",
        "Starting Well",
        "Enhanced Health in Care Homes",
        "Collaboration in Local Care Networks"
    )

    flexible_commissioning = fields.CharField(
        max_length=255,
        blank=True,
        null=True,
        choices=FLEXIBLE_FLAGS,
        verbose_name="Flexible commissioning"
    )


class Fp17IncompleteTreatment(models.EpisodeSubrecord):
    _is_singleton = True

    BAND_1 = "Band 1"
    BAND_2 = "Band 2"
    BAND_3 = "Band 3"

    TREATMENT_CATEGORIES = enum(
        BAND_1,
        BAND_2,
        BAND_3,
    )

    incomplete_treatment = fields.CharField(
        max_length=255, blank=True, null=True, choices=TREATMENT_CATEGORIES
    )

    date_of_acceptance = fields.DateField(
        blank=True, null=True,
        verbose_name="Date of acceptance"
    )
    completion_or_last_visit = fields.DateField(
        blank=True, null=True,
        verbose_name="Completion or last visit"
    )

    class Meta:
        verbose_name = "Incomplete treatment and treatment dates"


class Fp17Exemptions(models.EpisodeSubrecord):
    _is_singleton = True

    patient_under_18 = fields.BooleanField(
        default=False,
        verbose_name="Patient under 18"
    )

    # only used by fp17Os
    commissioner_approval = fields.BooleanField(
        default=False
    )
    full_remission_hc2_cert = fields.BooleanField(
        default=False,
        verbose_name = "Full remission - HC2 cert."
    )
    partial_remission_hc3_cert = fields.BooleanField(
        default=False,
        verbose_name="Partial remission - HC3 cert."
    )
    expectant_mother = fields.BooleanField(
        default=False,
        verbose_name="Expectant mother"
    )
    nursing_mother = fields.BooleanField(
        default=False,
        verbose_name="Nursing mother"
    )
    aged_18_in_full_time_education = fields.BooleanField(
        default=False,
        verbose_name="Aged 18 in full time education"
    )
    income_support = fields.BooleanField(
        default=False,
        verbose_name="Income support"
    )
    nhs_tax_credit_exemption = fields.BooleanField(
        default=False,
        verbose_name="NHS tax credit exemption"
    )
    income_based_jobseekers_allowance = fields.BooleanField(
        default=False,
        verbose_name="Income based jobseekers allowance"
    )
    pension_credit_guarantee_credit = fields.BooleanField(
        default=False,
        verbose_name="Pension credit guarantee credit"
    )
    prisoner = fields.BooleanField(default=False)
    universal_credit = fields.BooleanField(
        default=False,
        verbose_name="Universal credit"
    )
    income_related_employment_and_support_allowance = fields.BooleanField(
        default=False,
        verbose_name="Income related employment and support allowance"
    )

    evidence_of_exception_or_remission_seen = fields.BooleanField(
        default=False,
        verbose_name="Evidence of exception or remission seen"
    )

    patient_charge_collected = fields.DecimalField(
        decimal_places=2, max_digits=5, blank=True, null=True,
        verbose_name="Patient charge collected"
    )

    class Meta:
        verbose_name = "Exemptions and remissions"

    def to_dict(self, *args, **kwargs):
        as_dict = super().to_dict(*args, **kwargs)
        if as_dict["patient_charge_collected"]:
            as_dict["patient_charge_collected"] = float(
                as_dict["patient_charge_collected"]
            )
        return as_dict


class Fp17TreatmentCategory(models.EpisodeSubrecord):
    _is_singleton = True

    BAND_1 = "Band 1"
    BAND_2 = "Band 2"
    BAND_3 = "Band 3"
    URGENT_TREATMENT = "Urgent treatment"
    REGULATION_11_REPLACEMENT_APPLIANCE = "Regulation 11 replacement appliance"
    PRESCRIPTION_ONLY = "Prescription only"
    DENTURE_REPAIRS = "Denture repairs"
    BRIDGE_REPAIRS = "Bridge repairs"
    ARREST_OF_BLEEDING = "Arrest of bleeding"
    REMOVAL_OF_SUTURES = "Removal of sutures"

    TREATMENT_CATEGORIES = enum(
        BAND_1,
        BAND_2,
        BAND_3,
        URGENT_TREATMENT,
        REGULATION_11_REPLACEMENT_APPLIANCE,
        PRESCRIPTION_ONLY,
        DENTURE_REPAIRS,
        BRIDGE_REPAIRS,
        ARREST_OF_BLEEDING,
        REMOVAL_OF_SUTURES,
    )

    treatment_category = fields.CharField(
        max_length=255, blank=True, null=True,
        choices=TREATMENT_CATEGORIES,
        verbose_name="Treatment category"
    )

    class Meta:
        verbose_name = "Treatment category"


class Fp17ClinicalDataSet(models.EpisodeSubrecord):
    _is_singleton = True
    HARD = "Hard"
    SOFT = "Soft"

    OCCLUSAL_APPLIANCE_OPTIONS = enum(
        HARD, SOFT
    )

    scale_and_polish = fields.BooleanField(
        default=False,
        verbose_name="Scale and polish"
    )
    fluoride_varnish = fields.BooleanField(
        default=False,
        verbose_name="Fluoride varnish"
    )
    fissure_sealants = fields.IntegerField(
        blank=True, null=True,
        verbose_name="Fissure sealants"
    )
    radiographs_taken = fields.IntegerField(
        blank=True, null=True,
        verbose_name="Radiographs taken"
    )

    endodontic_treatment = fields.IntegerField(
        blank=True, null=True,
        verbose_name="Endontic treatment"
    )
    permanent_fillings = fields.IntegerField(
        blank=True, null=True,
        verbose_name="Permanent fillings"
    )
    extractions = fields.IntegerField(blank=True, null=True)
    crowns_provided = fields.IntegerField(
        blank=True, null=True,
        verbose_name="Crowns provided"
    )

    upper_denture_acrylic = fields.IntegerField(
        blank=True, null=True,
        verbose_name="Upper denture acrylic"
    )
    lower_denture_acrylic = fields.IntegerField(
        blank=True, null=True,
        verbose_name="Lower denture acrylic"
    )
    upper_denture_metal = fields.IntegerField(
        blank=True, null=True,
        verbose_name="Upper denture metal"
    )
    lower_denture_metal = fields.IntegerField(
        blank=True, null=True,
        verbose_name="Lower denture metal"
    )

    veneers_applied = fields.IntegerField(
        blank=True, null=True,
        verbose_name="Veneers applied"
    )
    inlays = fields.IntegerField(blank=True, null=True)
    bridges_fitted = fields.IntegerField(
        blank=True, null=True,
        verbose_name="Bridges fitted"
    )
    referral_for_advanced_mandatory_services_band = fields.IntegerField(
        blank=True, null=True,
        verbose_name="Referral for advanced mandatory services band"
    )

    examination = fields.BooleanField(default=False)
    antibiotic_items_prescribed = fields.IntegerField(
        blank=True, null=True,
        verbose_name="Antibiotic items prescribed"
    )
    other_treatment = fields.BooleanField(
        default=False,
        verbose_name="Other treatment"
    )
    best_practice_prevention = fields.BooleanField(
        default=False,
        verbose_name="Best practice prevention according to Delivering Better Oral Health offered"
    )

    decayed_teeth_permanent = fields.IntegerField(
        blank=True, null=True,
        verbose_name="Decayed teeth permanent"
    )
    decayed_teeth_deciduous = fields.IntegerField(
        blank=True, null=True,
        verbose_name="Decayed teeth deciduous"
    )
    missing_teeth_permanent = fields.IntegerField(
        blank=True, null=True,
        verbose_name="Missing teeth permanent"
    )
    missing_teeth_deciduous = fields.IntegerField(
        blank=True, null=True,
        verbose_name="Missing teeth deciduous"
    )
    filled_teeth_permanent = fields.IntegerField(
        blank=True, null=True,
        verbose_name="Filled teeth permanent"
    )
    filled_teeth_deciduous = fields.IntegerField(
        blank=True, null=True,
        verbose_name="Filled teeth deciduous"
    )
    pre_formed_crowns = fields.IntegerField(
        blank=True, null=True,
        verbose_name="Pre-Formed Crowns"
    )
    advanced_perio_root_surface_debridement = fields.IntegerField(
        blank=True, null=True,
        verbose_name="Advanced perio root surface debridement"
    )
    aerosol_generating_procedures = fields.IntegerField(
        blank=True, null=True
    )
    custom_made_occlusal_appliance = fields.CharField(
        blank=True,
        null=True,
        choices=OCCLUSAL_APPLIANCE_OPTIONS,
        max_length=256,
        verbose_name="Custom made occlusal appliance",
    )
    denture_additions_reline_rebase = fields.BooleanField(
        default=False, verbose_name="Denture Additions/Reline/Rebase"
    )
    phased_treatment = fields.BooleanField(
        default=False, verbose_name="Phased treatment"
    )

    class Meta:
        verbose_name = "Clinical data set"


class Fp17OtherDentalServices(models.EpisodeSubrecord):
    _is_singleton = True
    _title = "FP17 Other Dental Services"

    treatment_on_referral = fields.BooleanField(
        default=False,
        verbose_name="Treatment on referral"
    )
    free_repair_or_replacement = fields.BooleanField(
        default=False,
        verbose_name="Free repair or replacement"
    )
    further_treatment_within_2_months = fields.BooleanField(
        default=False,
        verbose_name="Further treatment within 2 months"
    )
    domicillary_services = fields.BooleanField(
        default=False,
        verbose_name="Domicillary services"
    )
    sedation_services = fields.BooleanField(
        default=False,
        verbose_name="Sedation services"
    )

    class Meta:
        verbose_name = "Other services"


class Fp17Recall(models.EpisodeSubrecord):
    _is_singleton = True

    number_of_months = fields.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = "NICE guidance"


class Fp17NHSBSAFields(models.EpisodeSubrecord):
    _is_singleton = True

    Fp17_NHSBSA_field_1 = fields.CharField(
        max_length=255, blank=True, null=True)
    Fp17_NHSBSA_field_2 = fields.CharField(
        max_length=255, blank=True, null=True)
    Fp17_NHSBSA_field_3 = fields.CharField(
        max_length=255, blank=True, null=True)
    Fp17_NHSBSA_field_4 = fields.DecimalField(
        decimal_places=2, max_digits=5, blank=True, null=True)


class Fp17Declaration(models.EpisodeSubrecord):
    _is_singleton = True

    class Meta:
        verbose_name = "Declaration"

    necessary_care_provided = fields.BooleanField(default=False)
    necessary_care_carried_out = fields.BooleanField(default=False)

    signature = fields.CharField(max_length=255, blank=True, null=True)
    signature_date = fields.DateField(blank=True, null=True)


# FP17O models
class OrthodonticDataSet(models.EpisodeSubrecord):
    _is_singleton = True

    PROPOSED = "Proposed"
    COMPLETED = "Completed / Abandoned / Discontinued Treatment"

    TREATMENT_TYPES = enum(PROPOSED, COMPLETED)

    # treatment type can be logically inferred from other fields.
    #
    # The docs say:
    # PROPOSED "Must be accompanied by Assess/Appliance Fitted"
    #
    #
    # COMPLETED "Must be accompanied by Treatment Abandoned (9161 1),
    # Treatment Discontinued (9161 2) or Treatment Completed (9161 3)"
    treatment_type            = fields.CharField(
        choices=TREATMENT_TYPES, max_length=255, blank=True, null=True
    )
    radiograph                      = fields.IntegerField(blank=True, null=True)
    removable_upper_appliance       = fields.BooleanField(default=False)
    removable_lower_appliance       = fields.BooleanField(default=False)
    fixed_upper_appliance           = fields.BooleanField(default=False)
    fixed_lower_appliance           = fields.BooleanField(default=False)
    function_appliance              = fields.BooleanField(default=False)
    retainer_upper                  = fields.BooleanField(default=False)
    retainer_lower                  = fields.BooleanField(default=False)
    aerosol_generating_procedures   = fields.IntegerField(blank=True, null=True)


class ExtractionChart(models.EpisodeSubrecord):
    """
    Dental charting uses Zsigmondy-Palmer notation.
    (https://en.wikipedia.org/wiki/Palmer_notation)

    Tl;dr: UR = Upper Right, etc; Numbers work up from the midline; Letters are deciduous.
    """
    _is_singleton = True

    ur_1 = fields.BooleanField(default=False)
    ur_2 = fields.BooleanField(default=False)
    ur_3 = fields.BooleanField(default=False)
    ur_4 = fields.BooleanField(default=False)
    ur_5 = fields.BooleanField(default=False)
    ur_6 = fields.BooleanField(default=False)
    ur_7 = fields.BooleanField(default=False)
    ur_8 = fields.BooleanField(default=False)
    ur_9 = fields.BooleanField(default=False)
    ur_a = fields.BooleanField(default=False)
    ur_b = fields.BooleanField(default=False)
    ur_c = fields.BooleanField(default=False)
    ur_d = fields.BooleanField(default=False)
    ur_e = fields.BooleanField(default=False)
    ul_1 = fields.BooleanField(default=False)
    ul_2 = fields.BooleanField(default=False)
    ul_3 = fields.BooleanField(default=False)
    ul_4 = fields.BooleanField(default=False)
    ul_5 = fields.BooleanField(default=False)
    ul_6 = fields.BooleanField(default=False)
    ul_7 = fields.BooleanField(default=False)
    ul_8 = fields.BooleanField(default=False)
    ul_9 = fields.BooleanField(default=False)
    ul_a = fields.BooleanField(default=False)
    ul_b = fields.BooleanField(default=False)
    ul_c = fields.BooleanField(default=False)
    ul_d = fields.BooleanField(default=False)
    ul_e = fields.BooleanField(default=False)
    lr_1 = fields.BooleanField(default=False)
    lr_2 = fields.BooleanField(default=False)
    lr_3 = fields.BooleanField(default=False)
    lr_4 = fields.BooleanField(default=False)
    lr_5 = fields.BooleanField(default=False)
    lr_6 = fields.BooleanField(default=False)
    lr_7 = fields.BooleanField(default=False)
    lr_8 = fields.BooleanField(default=False)
    lr_9 = fields.BooleanField(default=False)
    lr_a = fields.BooleanField(default=False)
    lr_b = fields.BooleanField(default=False)
    lr_c = fields.BooleanField(default=False)
    lr_d = fields.BooleanField(default=False)
    lr_e = fields.BooleanField(default=False)
    ll_1 = fields.BooleanField(default=False)
    ll_2 = fields.BooleanField(default=False)
    ll_3 = fields.BooleanField(default=False)
    ll_4 = fields.BooleanField(default=False)
    ll_5 = fields.BooleanField(default=False)
    ll_6 = fields.BooleanField(default=False)
    ll_7 = fields.BooleanField(default=False)
    ll_8 = fields.BooleanField(default=False)
    ll_9 = fields.BooleanField(default=False)
    ll_a = fields.BooleanField(default=False)
    ll_b = fields.BooleanField(default=False)
    ll_c = fields.BooleanField(default=False)
    ll_d = fields.BooleanField(default=False)
    ll_e = fields.BooleanField(default=False)


    def has_extractions(self):
        quadrents = ["ur", "lr", "ll", "ul"]
        permanent_teeth = list(range(1, 10))
        deciduous_teeth = ["a", "b", "c", "d", "e"]
        teeth = permanent_teeth + deciduous_teeth

        for quadrant in quadrents:
            for tooth in teeth:
                tooth_field = f"{quadrant}_{tooth}"
                if getattr(self, tooth_field) == True:
                    return True

class OrthodonticAssessment(models.EpisodeSubrecord):
    _is_singleton = True

    ASSESSMENT_AND_REVIEW = "Assessment & review"
    ASSESS_AND_REFUSE_TREATMENT = "Assess & refuse treatment"
    ASSESS_AND_APPLIANCE_FITTED = "Assess & appliance fitted"

    ASSESSMENT_CHOICES = (
        (ASSESSMENT_AND_REVIEW, ASSESSMENT_AND_REVIEW,),
        (ASSESS_AND_REFUSE_TREATMENT, ASSESS_AND_REFUSE_TREATMENT,),
        (ASSESS_AND_APPLIANCE_FITTED, ASSESS_AND_APPLIANCE_FITTED,),
    )
    IOTN_NOT_APPLICABLE = "N/A"

    IOTN_CHOICES = (
        ("1", "1",),
        ("2", "2",),
        ("3", "3",),
        ("4", "4",),
        ("5", "5",),
        (IOTN_NOT_APPLICABLE, IOTN_NOT_APPLICABLE,),
    )

    assessment = fields.CharField(
        choices=ASSESSMENT_CHOICES,
        blank=True,
        null=True,
        max_length=256,
        verbose_name="Assessment Type"
    )

    iotn = fields.CharField(
        choices=IOTN_CHOICES,
        blank=True,
        null=True,
        max_length=256,
        verbose_name="IOTN"
    )

    # Only accepts 1-10
    aesthetic_component = fields.IntegerField(
        blank=True, null=True
    )
    date_of_referral = fields.DateField(blank=True, null=True)
    date_of_assessment = fields.DateField(blank=True, null=True)
    date_of_appliance_fitted = fields.DateField(blank=True, null=True)


class OrthodonticTreatment(models.EpisodeSubrecord):

    class Meta:
        verbose_name = "Orthodontic Completion"

    _is_singleton = True

    PATIENT_FAILED_TO_RETURN = "Treatment abandoned - patient failed to return"
    PATIENT_REQUESTED = "Treatment abandoned - patient requested"
    TREATMENT_DISCONTINUED = "Treatment discontinued"
    TREATMENT_COMPLETED = "Treatment completed"

    COMPLETION_TYPE_CHOICES = (
        (TREATMENT_COMPLETED, TREATMENT_COMPLETED,),
        (TREATMENT_DISCONTINUED, TREATMENT_DISCONTINUED,),
        (PATIENT_REQUESTED, PATIENT_REQUESTED,),
        (PATIENT_FAILED_TO_RETURN, PATIENT_FAILED_TO_RETURN,),
    )

    IOTN_NOT_APPLICABLE = "N/A"

    IOTN_CHOICES = (
        ("1", "1",),
        ("2", "2",),
        ("3", "3",),
        ("4", "4",),
        ("5", "5",),
        (IOTN_NOT_APPLICABLE, IOTN_NOT_APPLICABLE,),
    )

    completion_type = fields.CharField(
        choices=COMPLETION_TYPE_CHOICES,
        null=True,
        blank=True,
        max_length=256,
    )

    iotn = fields.CharField(
        choices=IOTN_CHOICES,
        blank=True,
        null=True,
        max_length=256,
        verbose_name="IOTN"
    )

    par_scores_calculated = fields.BooleanField(
        default=False,
        verbose_name="PAR "
    )
    # Only accepts 1-10
    aesthetic_component = fields.IntegerField(
        blank=True, null=True
    )
    repair = fields.BooleanField(
        default=False,
        verbose_name="Repair to appliance fitted by another dentist"
    )
    replacement = fields.BooleanField(
        default=False,
        verbose_name="Regulation 11 replacement appliance"
    )
    date_of_completion = fields.DateField(
        blank=True,
        null=True,
        verbose_name="Date of completion or last visit"
    )


class CaseMix(models.EpisodeSubrecord):
    """
    Case mix is a way of gauging the complexity of
    patients as laid out by
    https://bda.org/dentists/governance-and-representation/craft-committees/salaried-primary-care-dentists/Documents/Case%20mix%202019.pdf  #NOQA E501
    """
    _is_singleton = True

    class Meta:
        verbose_name = "Case mix"
        verbose_name_plural = "Case mixes"

    CASE_MIX_FIELDS = {
        "ability_to_communicate": {
            "0": 0, "A": 2, "B": 4, "C": 8
        },
        "ability_to_cooperate": {
            "0": 0, "A": 3, "B": 6, "C": 12
        },
        "medical_status": {
            "0": 0, "A": 2, "B": 6, "C": 12
        },
        "oral_risk_factors": {
            "0": 0, "A": 3, "B": 6, "C": 12
        },
        "access_to_oral_care": {
            "0": 0, "A": 2, "B": 4, "C": 8
        },
        "legal_and_ethical_barriers_to_care": {
            "0": 0, "A": 2, "B": 4, "C": 8
        }
    }

    STANDARD_PATIENT = "Standard patient"
    SOME_COMPLEXITY = "Some complexity"
    MODERATE_COMPLEXITY = "Moderate complexity"
    SEVERE_COMPLEXITY = "Severe complexity"
    EXTREME_COMPLEXITY = "Extreme complexity"

    CHOICES = enum("0", "A", "B", "C")
    ability_to_communicate = fields.CharField(
        blank=True,
        null=True,
        max_length=256,
        choices=CHOICES,
        verbose_name="Ability to communicate"
    )
    ability_to_cooperate = fields.CharField(
        blank=True,
        null=True,
        max_length=256,
        choices=CHOICES,
        verbose_name="Ability to co-operate"
    )
    medical_status = fields.CharField(
        blank=True,
        null=True,
        max_length=256,
        choices=CHOICES,
        verbose_name="Medical status"
    )
    oral_risk_factors = fields.CharField(
        blank=True,
        null=True,
        max_length=256,
        choices=CHOICES,
        verbose_name="Oral risk factors"
    )
    access_to_oral_care = fields.CharField(
        blank=True,
        null=True,
        max_length=256,
        choices=CHOICES,
        verbose_name="Access to oral care"
    )
    legal_and_ethical_barriers_to_care = fields.CharField(
        blank=True,
        null=True,
        max_length=256,
        choices=CHOICES,
        verbose_name="Legal and ethical barriers to care"
    )

    def max_code(self):
        val = 0
        code = "0"
        for field, mapping in self.CASE_MIX_FIELDS.items():
            val = getattr(self, field)

    def score(self, field):
        val = getattr(self, field)
        if val is not None:
            return self.CASE_MIX_FIELDS[field][val]

    def total_score(self):
        total = 0
        for field in self.CASE_MIX_FIELDS.keys():
            score = self.score(field)
            if score:
                total += score
        return total

    def band(self):
        total = self.total_score()

        if total == 0:
            return self.STANDARD_PATIENT
        if total < 10:
            return self.SOME_COMPLEXITY
        if total < 20:
            return self.MODERATE_COMPLEXITY
        if total < 30:
            return self.SEVERE_COMPLEXITY
        return self.EXTREME_COMPLEXITY


class CovidTriage(models.EpisodeSubrecord):
    """
    Triage models are the data used by the covid
    triage episode category.

    They store data about patient interaction
    where there is not going to be an FP17 or FP17O
    """
    _is_singleton = True

    class Meta:
        verbose_name = "COVID-19 triage"

    # Order is important for the choices
    # the code sent to compass is the idx + 1
    LOCAL_UCD_REFERRAL_REASONS = enum(
        "Life threatening emergencies",
        "Trauma",
        "Oro-facial swelling",
        "Post extraction bleeding",
        "Dental conditions resulting in systematic illness",
        "Severe dental or facial pain",
        "Fractured teeth with pulp exposure",
        "Dental and soft tissue infections",
        "Suspected oral cancer",
        "Oro-dental conditions worsening systemic illness"
    )

    COVID_STATUS = enum(
        "Patient is shielded",
        "Increased risk of illness from COVID-19",
        "Possible/confirmed COVID-19 patient (or those living in household)",
        "Other",
        "Patient is COVID-19 symptom free at present"
    )

    REASONS_FOR_THE_CALL = enum(
        "Pain",
        "Swelling",
        "Bleeding",
        "Trauma",
        "Soft tissue pathology",
        "Other",
        "Routine treatment"
    )
    FP17 = "FP17"
    FP17O = "FP17O"
    TRIAGE_TYPE = enum(FP17, FP17O)
    triage_type = fields.CharField(
        blank=True,
        null=True,
        choices=TRIAGE_TYPE,
        max_length=256
    )
    datetime_of_contact = fields.DateTimeField(
        verbose_name="Date of contact",
        blank=True,
        null=True,
    )
    dental_care_professional = fields.BooleanField(
        default=False,
        verbose_name="Carried out by a dental care professional"
    )
    primary_reason = fields.CharField(
        blank=True,
        null=True,
        max_length=256,
        verbose_name='Primary reason for call',
        choices=REASONS_FOR_THE_CALL
    )
    covid_status = fields.CharField(
        blank=True,
        null=True,
        max_length=256,
        verbose_name="COVID-19 status",
        choices=COVID_STATUS
    )
    triage_via_video = fields.BooleanField(
        default=False,
        verbose_name="Triage via video"
    )
    advice_given = fields.BooleanField(
        default=False, verbose_name="Advice given"
    )
    advised_analgesics = fields.BooleanField(
        default=False, verbose_name="Advised analgesics"
    )
    remote_prescription_analgesics = fields.BooleanField(
        default=False,
        verbose_name="Remote prescription of analgesics"
    )
    remote_prescription_antibiotics = fields.BooleanField(
        default=False,
        verbose_name="Remote prescription of antibiotics"
    )
    follow_up_call_required = fields.BooleanField(
        default=False,
        verbose_name="Follow up call required"
    )
    call_back_if_symptoms_worsen = fields.BooleanField(
        default=False,
        verbose_name="Recommended a call back if symptoms worsened"
    )
    referrered_to_local_udc_reason = fields.CharField(
        blank=True,
        null=True,
        max_length=256,
        choices=LOCAL_UCD_REFERRAL_REASONS,
        verbose_name="Reason the patient has been referred to the local urgent \
dental care centre"
    )
    face_to_face_appointment = fields.BooleanField(
        default=False,
        verbose_name="The triage call recommended a face to face but patient failed to attend"
    )
