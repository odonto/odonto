"""
odonto models.
"""
from django.db.models import fields

from opal import models

"""
Core Opal models - these inherit from the abstract data models in
opal.models but can be customised here with extra / altered fields.
"""
class Location(models.Location): pass
class Allergies(models.Allergies): pass
class Diagnosis(models.Diagnosis): pass
class PastMedicalHistory(models.PastMedicalHistory): pass
class Treatment(models.Treatment): pass
class Investigation(models.Investigation): pass
class SymptomComplex(models.SymptomComplex): pass
class PatientConsultation(models.PatientConsultation): pass

# we commonly need a referral route, ie how the patient
# came to the service, but not always.
# class ReferralRoute(models.ReferralRoute): pass


"""
End Opal core models
"""


class Demographics(models.Demographics):
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

    house_number_or_name = fields.CharField(max_length=255, null=True, blank=True)
    street               = fields.CharField(max_length=255, null=True, blank=True)
    city_or_town         = fields.CharField(max_length=255, null=True, blank=True)
    county               = fields.CharField(max_length=255, null=True, blank=True)

    # postcode = fields.CharField(max_length=255)  # => opal.Demographics.postcode


class Fp17DentalCareProvider(models.PatientSubrecord):
    _is_singleton = True
    _title = "Provider details"
    # I'm pretty sure this should not be handled as a PatientSubrecord
    # but I'm not sure what it /should/ be
    # the following provider information is not currently in an Opal model
    # ^^^ consider splitting this into a Provider Model
    provider_name            = fields.CharField(max_length=255, blank=True, null=True)
    provider_location_number = fields.CharField(max_length=255, blank=True, null=True)
    provider_address         = fields.CharField(max_length=255, blank=True, null=True)
    performer_number         = fields.CharField(max_length=255, blank=True, null=True)


class Fp17IncompleteTreatment(models.EpisodeSubrecord):
    _is_singleton = True
    _title = 'FP17 Treatment Course'

    incomplete_treatment_band_1 = fields.BooleanField(default=False)
    incomplete_treatment_band_2 = fields.BooleanField(default=False)
    incomplete_treatment_band_3 = fields.BooleanField(default=False)
    date_of_acceptance          = fields.DateField(blank=True, null=True)
    completion_or_last_visit    = fields.DateField(blank=True, null=True)


class Fp17Exemptions(models.EpisodeSubrecord):
    _is_singleton = True
    _title = "Exemptions and Remissions"

    patient_under_18                  = fields.BooleanField(default=False)
    full_remission_hc2_cert           = fields.BooleanField(default=False)
    partial_remission_hc3_cert        = fields.BooleanField(default=False)
    expectant_mother                  = fields.BooleanField(default=False)
    nursing_mother                    = fields.BooleanField(default=False)
    aged_18_in_full_time_education    = fields.BooleanField(default=False)
    income_support                    = fields.BooleanField(default=False)
    nhs_tax_credit_exemption          = fields.BooleanField(default=False)
    income_based_jobseekers_allowance = fields.BooleanField(default=False)
    pension_credit_guarantee_credit   = fields.BooleanField(default=False)
    prisoner                          = fields.BooleanField(default=False)
    universal_credit                  = fields.BooleanField(default=False)
    evidence_of_exception_or_remission_seen = fields.BooleanField(default=False)
    income_related_employment_and_support_allowance = fields.BooleanField(default=False)

    # logically I'd like to split this into its own PatientRemittance model
    # to keep all the Exemptions cleanly together in their own Model.
    patient_charge_collected = fields.DecimalField(decimal_places=2, max_digits=5, blank=True, null=True)


class Fp17TreatmentCategory(models.EpisodeSubrecord):
    _is_singleton = True
    _title = "Treatment Category"

    treatment_category_band_1           = fields.BooleanField(default=False)
    treatment_category_band_2           = fields.BooleanField(default=False)
    treatment_category_band_3           = fields.BooleanField(default=False)
    urgent_treatment                    = fields.BooleanField(default=False)
    regulation_11_replacement_appliance = fields.BooleanField(default=False)
    prescription_only                   = fields.BooleanField(default=False)
    denture_repairs                     = fields.BooleanField(default=False)
    bridge_repairs                      = fields.BooleanField(default=False)
    arrest_of_bleeding                  = fields.BooleanField(default=False)
    removal_of_sutures                  = fields.BooleanField(default=False)


class Fp17ClinicalDataSet(models.EpisodeSubrecord):
    _is_singleton = True
    _title = "FP17 Clinical Data Set"

    scale_and_polish  = fields.BooleanField(default=False)
    fluoride_varnish  = fields.BooleanField(default=False)
    fissure_sealants  = fields.IntegerField(blank=True, null=True)
    radiographs_taken = fields.IntegerField(blank=True, null=True)

    endodontic_treatment = fields.BooleanField(default=False)
    permanent_fillings_and_sealant_restorations = fields.IntegerField(blank=True, null=True)
    extractions     = fields.IntegerField(blank=True, null=True)
    crowns_provided = fields.IntegerField(blank=True, null=True)

    upper_denture_acrylic = fields.IntegerField(blank=True, null=True)
    lower_denture_acrylic = fields.IntegerField(blank=True, null=True)
    upper_denture_metal   = fields.IntegerField(blank=True, null=True)
    lower_denture_metal   = fields.IntegerField(blank=True, null=True)

    veneers_applied = fields.IntegerField(blank=True, null=True)
    inlays          = fields.IntegerField(blank=True, null=True)
    bridges_fitted  = fields.IntegerField(blank=True, null=True)
    referral_for_advanced_mandatory_services_band = fields.IntegerField(blank=True, null=True)

    examination                 = fields.BooleanField(default=False)
    antibiotic_items_prescribed = fields.IntegerField(blank=True, null=True)
    other_treatment             = fields.BooleanField(default=False)
    best_practice_prevention_according_to_delivering_better_oral_health_offered = fields.BooleanField(default=False)

    decayed_teeth_permanent = fields.IntegerField(blank=True, null=True)
    decayed_teeth_deciduous = fields.IntegerField(blank=True, null=True)
    missing_teeth_permanent = fields.IntegerField(blank=True, null=True)
    missing_teeth_deciduous = fields.IntegerField(blank=True, null=True)
    filled_teeth_permanent  = fields.IntegerField(blank=True, null=True)
    filled_teeth_deciduous  = fields.IntegerField(blank=True, null=True)


class Fp17OtherDentalServices(models.EpisodeSubrecord):
    _is_singleton = True
    _title = "FP17 Other Dental Services"

    treatment_on_referral             = fields.BooleanField(default=False)
    free_repair_or_replacement        = fields.BooleanField(default=False)
    further_treatment_within_2_months = fields.BooleanField(default=False)
    domicillary_services              = fields.BooleanField(default=False)
    sedation_services                 = fields.BooleanField(default=False)


class Fp17Recall(models.EpisodeSubrecord):
    _is_singleton = True

    number_of_months = fields.IntegerField(blank=True, null=True)


class Fp17NHSBSAFields(models.EpisodeSubrecord):
    _is_singleton = True

    Fp17_NHSBSA_field_1 = fields.CharField(max_length=255, blank=True, null=True)
    Fp17_NHSBSA_field_2 = fields.CharField(max_length=255, blank=True, null=True)
    Fp17_NHSBSA_field_3 = fields.CharField(max_length=255, blank=True, null=True)
    Fp17_NHSBSA_field_4 = fields.DecimalField(decimal_places=2, max_digits=5, blank=True, null=True)


class Fp17Declaration(models.EpisodeSubrecord):
    _is_singleton = True

    necessary_care_provided    = fields.BooleanField(default=False)
    necessary_care_carried_out = fields.BooleanField(default=False)

    signature                  = fields.CharField(max_length=255, blank=True, null=True)
    signature_date             = fields.DateField(blank=True, null=True)
