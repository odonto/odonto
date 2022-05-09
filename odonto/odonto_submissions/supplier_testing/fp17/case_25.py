import datetime
from odonto.odonto_submissions.serializers import translate_to_bdcs1
from fp17 import treatments


def annotate(bcds1):
    bcds1.patient.surname = "CHESTER"
    bcds1.patient.forename = "EDWARD"
    bcds1.patient.address = ["25 HIGH STREET"]
    bcds1.patient.sex = 'M'
    bcds1.patient.nhs_number = '0000000000'
    bcds1.patient.date_of_birth = datetime.date(1940, 12, 2)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 1)

    # Treatments: "Ethnic Origin 8"
    bcds1.treatments = [
        treatments.ETHNIC_ORIGIN_8_ASIAN_OR_ASIAN_BRITISH_INDIAN,
        treatments.SEDATION_SERVICES,
    ]

    return bcds1


def from_model(bcds1, patient, episode):
    demographics = patient.demographics()
    demographics.surname = "CHESTER"
    demographics.first_name = "EDWARD"
    demographics.house_number_or_name = "25"
    demographics.street = "HIGH STREET"
    demographics.sex = "Male"
    demographics.date_of_birth = datetime.date(1940, 12, 2)
    demographics.ethnicity = "Asian or asian british indian"
    demographics.save()

    episode.fp17otherdentalservices_set.update(
        sedation_services=True
    )

    episode.fp17incompletetreatment_set.update(
        date_of_acceptance=datetime.date(2017, 4, 1),
        completion_or_last_visit=datetime.date(2017, 4, 1)
    )
    translate_to_bdcs1(bcds1, episode)
