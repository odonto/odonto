import datetime
from odonto.odonto_submissions.serializers import translate_to_bdcs1
from fp17 import treatments


def annotate(bcds1):
    bcds1.patient.surname = "ASTON"
    bcds1.patient.forename = "ZARA"
    bcds1.patient.address = ["33 HIGH STREET"]
    bcds1.patient.sex = 'F'
    bcds1.patient.nhs_number = '0000000000'
    bcds1.patient.date_of_birth = datetime.date(1960, 6, 26)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 1)

    bcds1.patient_charge_pence = 5630

    # Treatments: "Extraction x 1, Ethnic Origin 99"
    bcds1.treatments = [
        treatments.TREATMENT_CATEGORY(2),
        treatments.EXTRACTION(1),
        treatments.ETHNIC_ORIGIN_PATIENT_DECLINED,
    ]

    return bcds1


def from_model(bcds1, patient, episode):
    demographics = patient.demographics()
    demographics.surname = "ASTON"
    demographics.first_name = "ZARA"
    demographics.house_number_or_name = "33"
    demographics.street = "HIGH STREET"
    demographics.sex = "Female"
    demographics.date_of_birth = datetime.date(1960, 6, 26)
    demographics.ethnicity = "Patient declined"
    demographics.save()

    episode.fp17exemptions_set.update(
        patient_charge_collected=56.30
    )

    episode.fp17treatmentcategory_set.update(
        treatment_category="Band 2",
    )

    episode.fp17clinicaldataset_set.update(
        extractions=1,
    )

    episode.fp17incompletetreatment_set.update(
        date_of_acceptance=datetime.date(2017, 4, 1),
        completion_or_last_visit=datetime.date(2017, 4, 1)
    )
    translate_to_bdcs1(bcds1, episode)
