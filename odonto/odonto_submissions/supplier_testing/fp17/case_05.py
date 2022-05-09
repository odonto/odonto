import datetime

from fp17 import treatments
from odonto import models
from odonto.odonto_submissions.serializers import translate_to_bdcs1


def annotate(bcds1):
    bcds1.patient.surname = "BEDWORTH"
    bcds1.patient.forename = "TOBY"
    bcds1.patient.address = ["5 HIGH STREET"]
    bcds1.patient.sex = 'M'
    bcds1.patient.nhs_number = '0000000000'
    bcds1.patient.date_of_birth = datetime.date(1938, 4, 11)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 1)

    bcds1.patient_charge_pence = 7320

    # Treatments: "Upper Acrylic Denture 12, Ethnic Origin 5"
    bcds1.treatments = [
        treatments.REGULATION_11_APPLIANCE,
        treatments.UPPER_DENTURE_ACRYLIC(12),
        treatments.ETHNIC_ORIGIN_5_WHITE_AND_BLACK_AFRICAN,
    ]

    return bcds1


def from_model(bcds1, patient, episode):
    demographics = patient.demographics()
    demographics.surname = "BEDWORTH"
    demographics.first_name = "TOBY"
    demographics.house_number_or_name = "5"
    demographics.street = "HIGH STREET"
    demographics.sex = "Male"
    demographics.date_of_birth = datetime.date(1938, 4, 11)
    demographics.ethnicity = "White and black african"
    demographics.save()
    episode.fp17treatmentcategory_set.update(
        treatment_category=models.Fp17TreatmentCategory.REGULATION_11_REPLACEMENT_APPLIANCE
    )

    episode.fp17clinicaldataset_set.update(
        upper_denture_acrylic=12
    )

    episode.fp17exemptions_set.update(
        patient_charge_collected="73.20"
    )

    episode.fp17incompletetreatment_set.update(
        date_of_acceptance=datetime.date(2017, 4, 1),
        completion_or_last_visit=datetime.date(2017, 4, 1)
    )

    translate_to_bdcs1(bcds1, episode)
