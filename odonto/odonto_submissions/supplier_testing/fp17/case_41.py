import datetime
from odonto.odonto_submissions.serializers import translate_to_bdcs1
from fp17 import treatments, exemptions


def annotate(bcds1):
    bcds1.patient.surname = "CARSTAIRS"
    bcds1.patient.forename = "EMMA"
    bcds1.patient.address = ["38 HIGH STREET"]
    bcds1.patient.sex = 'F'
    bcds1.patient.nhs_number = '0000000000'
    bcds1.patient.date_of_birth = datetime.date(1990, 6, 21)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 1)

    # "Prisoner"
    bcds1.exemption_remission = {
        'code': exemptions.PRISONER,
    }

    # Treatments: "None"
    bcds1.treatments = [
        treatments.TREATMENT_CATEGORY(1),
        treatments.ETHNIC_ORIGIN_PATIENT_DECLINED,
    ]

    return bcds1


def from_model(bcds1, patient, episode):
    demographics = patient.demographics()
    demographics.surname = "CARSTAIRS"
    demographics.first_name = "EMMA"
    demographics.house_number_or_name = "38"
    demographics.street = "HIGH STREET"
    demographics.sex = "Female"
    demographics.date_of_birth = datetime.date(1990, 6, 21)
    demographics.ethnicity = "Patient declined"
    demographics.save()

    episode.fp17treatmentcategory_set.update(
        treatment_category="Band 1",
    )

    episode.fp17exemptions_set.update(
        prisoner=True
    )

    episode.fp17incompletetreatment_set.update(
        date_of_acceptance=datetime.date(2017, 4, 1),
        completion_or_last_visit=datetime.date(2017, 4, 1)
    )
    translate_to_bdcs1(bcds1, episode)
