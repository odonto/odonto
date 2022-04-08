import datetime

from fp17 import treatments
from odonto.odonto_submissions.serializers import translate_to_bdcs1


def annotate(bcds1):
    bcds1.patient.surname = "BARNT"
    bcds1.patient.forename = "ANNIE"
    bcds1.patient.address = ["2 HIGH STREET"]
    bcds1.patient.sex = 'F'
    bcds1.patient.nhs_number = '0000000000'
    bcds1.patient.date_of_birth = datetime.date(1985, 7, 5)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 1)

    bcds1.patient_charge_pence = 5630

    # Treatments: "Filling x 1, Recall Interval 6, Ethnic Origin 2"
    bcds1.treatments = [
        treatments.TREATMENT_CATEGORY(2),
        treatments.RECALL_INTERVAL(num_months=6),
        treatments.ETHNIC_ORIGIN_2_WHITE_IRISH,
    ]

    return bcds1


def from_model(bcds1, patient, episode):
    demographics = patient.demographics()
    demographics.surname = "BARNT"
    demographics.first_name = "ANNIE"
    demographics.house_number_or_name = "2"
    demographics.street = "HIGH STREET"
    demographics.sex = "Female"
    demographics.date_of_birth = datetime.date(1985, 7, 5)
    demographics.ethnicity = "White irish"
    demographics.save()
    episode.fp17treatmentcategory_set.update(
        treatment_category="Band 2",
    )
    episode.fp17recall_set.update(
        number_of_months=6
    )

    episode.fp17incompletetreatment_set.update(
        date_of_acceptance=datetime.date(2017, 4, 1),
        completion_or_last_visit=datetime.date(2017, 4, 1)
    )
    episode.fp17exemptions_set.update(
        patient_charge_collected="56.30"
    )
    translate_to_bdcs1(bcds1, episode)
