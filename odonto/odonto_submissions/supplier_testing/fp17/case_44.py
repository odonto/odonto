import datetime
from odonto.odonto_submissions.serializers import translate_to_bdcs1
from fp17 import treatments


def annotate(bcds1):
    bcds1.patient.surname = "BORAGE"
    bcds1.patient.forename = "ARNOLD"
    bcds1.patient.address = ["41 HIGH STREET"]
    bcds1.patient.sex = 'M'
    bcds1.patient.nhs_number = '0000000000'
    bcds1.patient.date_of_birth = datetime.date(1935, 11, 17)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 5, 1)

    bcds1.patient_charge_pence = 24430

    # Treatments: "Crowns x 2, Missing Permanent 8"
    bcds1.treatments = [
        treatments.TREATMENT_CATEGORY(3),
        treatments.ETHNIC_ORIGIN_PATIENT_DECLINED,
    ]

    return bcds1


def from_model(bcds1, patient, episode):
    demographics = patient.demographics()
    demographics.surname = "BORAGE"
    demographics.first_name = "ARNOLD"
    demographics.house_number_or_name = "41"
    demographics.street = "HIGH STREET"
    demographics.sex = "Male"
    demographics.ethnicity = "Patient declined"
    demographics.date_of_birth = datetime.date(1935, 11, 17)
    demographics.save()

    episode.fp17exemptions_set.update(
        patient_charge_collected=244.30
    )

    episode.fp17treatmentcategory_set.update(
        treatment_category="Band 3",
    )

    episode.fp17incompletetreatment_set.update(
        date_of_acceptance=datetime.date(2017, 4, 1),
        completion_or_last_visit=datetime.date(2017, 5, 1)
    )

    translate_to_bdcs1(bcds1, episode)
