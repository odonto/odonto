import datetime
from odonto import models
from odonto.odonto_submissions.serializers import translate_to_bdcs1
from fp17 import treatments


def annotate(bcds1):
    bcds1.patient.surname = "ASLOCKTON"
    bcds1.patient.forename = "LAURA"
    bcds1.patient.address = ["32 HIGH STREET"]
    bcds1.patient.sex = 'F'
    bcds1.patient.nhs_number = '0000000000'
    bcds1.patient.date_of_birth = datetime.date(1968, 3, 24)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 1)

    bcds1.patient_charge_pence = 2060

    # Treatments: "Other Treatment (9399), Ethnic Origin 99"
    bcds1.treatments = [
        treatments.TREATMENT_CATEGORY_URGENT,
        treatments.OTHER_TREATMENT,
        treatments.ETHNIC_ORIGIN_PATIENT_DECLINED,
    ]

    return bcds1


def from_model(bcds1, patient, episode):
    demographics = patient.demographics()
    demographics.surname = "ASLOCKTON"
    demographics.first_name = "LAURA"
    demographics.house_number_or_name = "32"
    demographics.street = "HIGH STREET"
    demographics.sex = "Female"
    demographics.date_of_birth = datetime.date(1968, 3, 24)
    demographics.ethnicity = "Patient declined"
    demographics.save()

    episode.fp17exemptions_set.update(
        patient_charge_collected=20.60
    )

    episode.fp17treatmentcategory_set.update(
        treatment_category=models.Fp17TreatmentCategory.URGENT_TREATMENT
    )

    episode.fp17clinicaldataset_set.update(
        other_treatment=True,
    )

    episode.fp17exemptions_set.update(
        patient_charge_collected=20.60
    )

    episode.fp17incompletetreatment_set.update(
        date_of_acceptance=datetime.date(2017, 4, 1),
        completion_or_last_visit=datetime.date(2017, 4, 1)
    )
    translate_to_bdcs1(bcds1, episode)
