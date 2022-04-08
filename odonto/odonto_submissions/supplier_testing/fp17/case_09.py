import datetime
from odonto import models
from odonto.odonto_submissions.serializers import translate_to_bdcs1
from fp17 import treatments


def annotate(bcds1):
    bcds1.patient.surname = "BESCOT"
    bcds1.patient.forename = "OLIVER"
    bcds1.patient.address = ["9 HIGH STREET"]
    bcds1.patient.sex = 'M'
    bcds1.patient.nhs_number = '0000000000'
    bcds1.patient.date_of_birth = datetime.date(1968, 7, 6)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 1)

    # Treatments: "Ethnic Origin 9"
    bcds1.treatments = [
        treatments.ARREST_OF_BLEEDING,
        treatments.ETHNIC_ORIGIN_9_ASIAN_OR_ASIAN_BRITISH_PAKISTANI,
    ]

    return bcds1


def from_model(bcds1, patient, episode):
    demographics = patient.demographics()
    demographics.surname = "BESCOT"
    demographics.first_name = "OLIVER"
    demographics.house_number_or_name = "9"
    demographics.street = "HIGH STREET"
    demographics.sex = "Male"
    demographics.date_of_birth = datetime.date(1968, 7, 6)
    demographics.ethnicity = "Asian or asian british pakistani"
    demographics.save()

    episode.fp17treatmentcategory_set.update(
        treatment_category=models.Fp17TreatmentCategory.ARREST_OF_BLEEDING
    )

    episode.fp17incompletetreatment_set.update(
        date_of_acceptance=datetime.date(2017, 4, 1),
        completion_or_last_visit=datetime.date(2017, 4, 1)
    )
    translate_to_bdcs1(bcds1, episode)
