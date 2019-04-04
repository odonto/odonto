"""
odonto models.
"""
from django.db.models import fields
from django.db import models as djangomodels

from opal import models
from opal.core.fields import enum

"""
Core Opal models - these inherit from the abstract data models in
opal.models but can be customised here with extra / altered fields.
"""


class Location(models.Location):
    pass


class Allergies(models.Allergies):
    pass


class Diagnosis(models.Diagnosis):
    pass


class PastMedicalHistory(models.PastMedicalHistory):
    pass


class Treatment(models.Treatment):
    pass


class Investigation(models.Investigation):
    pass


class SymptomComplex(models.SymptomComplex):
    pass


class PatientConsultation(models.PatientConsultation):
    pass

# we commonly need a referral route, ie how the patient
# came to the service, but not always.
# class ReferralRoute(models.ReferralRoute): pass


"""
End Opal core models
"""

class PerformerNumber(djangomodels.Model):
    user   = djangomodels.ForeignKey(
        models.User, on_delete=djangomodels.CASCADE
    )
    number = fields.TextField()


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
    city_or_town = fields.CharField(
        max_length=255, null=True, blank=True,
        verbose_name="City or town"
    )
    county = fields.CharField(max_length=255, null=True, blank=True)

    # post_code = fields.CharField(max_length=255)  # => opal.Demographics.post_code
    class Meta:
        verbose_name = "Patient information"

class Fp17DentalCareProvider(models.PatientSubrecord):
    _is_singleton = True

    LOCATION_NUMBERS = (
        ('010108', 'Albion Road'),
        ('010112', 'Amble'),
        ('010113', 'Blyth'),
        ('016027', 'Hexham'),
        ('010109', 'Longbenton'),
        ('24946', 'Morpeth NHS Centre'),
        ('010117', 'Northgate'),
        ('010116', 'Seaton Hirst'),
        ('010111', 'Wallsend'),
        ('010054', 'Ward 15, WGH'),
    )

    # I'm pretty sure this should not be handled as a PatientSubrecord
    # but I'm not sure what it /should/ be
    # the following provider information is not currently in an Opal model
    # ^^^ consider splitting this into a Provider Model
    provider_name = fields.CharField(
        max_length=255, blank=True, null=True,
        verbose_name="Provider name"
    )
    provider_location_number = fields.CharField(
        max_length=255, blank=True, null=True,
        verbose_name="Provider location",
        choices=LOCATION_NUMBERS
    )
    provider_address = fields.CharField(
        max_length=255, blank=True, null=True,
        verbose_name="Provider address"
    )
    performer = fields.CharField(
        max_length=255, blank=True, null=True
    )

    class Meta:
        verbose_name = "Part 1 Provider name, address and location"


class Fp17IncompleteTreatment(models.EpisodeSubrecord):
    _is_singleton = True

    BAND_CHOICES = enum('Band 1', 'Band 2', 'Band 3')

    treatment_band = fields.CharField(
        max_length=255, blank=True, null=True,
        choices=BAND_CHOICES
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
        verbose_name = "Part 3 Incomplete treatment and treatment dates"


class Fp17Exemptions(models.EpisodeSubrecord):
    _is_singleton = True

    patient_under_18 = fields.BooleanField(
        default=False,
        verbose_name="Patient under 18"
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
        verbose_name = "Part 4 Exemptions and remissions"


class Fp17TreatmentCategory(models.EpisodeSubrecord):
    _is_singleton = True

    TREATMENT_CATEGORIES = enum(
        "Band 1", "Band 2", "Band 3"
    )

    treatment_category = fields.CharField(
        max_length=255, blank=True, null=True,
        choices=TREATMENT_CATEGORIES,
        verbose_name="Treatment category"
    )
    urgent_treatment = fields.BooleanField(
        default=False,
        verbose_name="Urgent treatment"
    )
    regulation_11_replacement_appliance = fields.BooleanField(
        default=False,
        verbose_name="Regulation 11 replacement appliance"
    )
    prescription_only = fields.BooleanField(
        default=False,
        verbose_name="Prescription only"
    )
    denture_repairs = fields.BooleanField(
        default=False,
        verbose_name="Denture repairs"
    )
    bridge_repairs = fields.BooleanField(
        default=False,
        verbose_name="Bridge repairs"
    )
    arrest_of_bleeding = fields.BooleanField(
        default=False,
        verbose_name="Arrest of bleeding"
    )
    removal_of_sutures = fields.BooleanField(
        default=False,
        verbose_name="Removal of sutures"
    )

    class Meta:
        verbose_name = "Part 5 Treatment category"


class Fp17ClinicalDataSet(models.EpisodeSubrecord):
    _is_singleton = True

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
    permanent_fillings_and_sealant_restorations = fields.IntegerField(
        blank=True, null=True,
        verbose_name="Permanent fillings and sealant restorations"
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

    class Meta:
        verbose_name="Part 5a Clinical data set"


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
        verbose_name = "Part 6 Other services"


class Fp17Recall(models.EpisodeSubrecord):
    _is_singleton = True

    number_of_months = fields.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = "Part 7 NICE guidance"


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

    necessary_care_provided = fields.BooleanField(default=False)
    necessary_care_carried_out = fields.BooleanField(default=False)

    signature = fields.CharField(max_length=255, blank=True, null=True)
    signature_date = fields.DateField(blank=True, null=True)
