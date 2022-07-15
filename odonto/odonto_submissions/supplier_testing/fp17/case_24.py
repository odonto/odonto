import datetime
from odonto.odonto_submissions.serializers import translate_to_bdcs1
from fp17 import treatments


def annotate(bcds1):
    bcds1.patient.surname = "CARLTON"
    bcds1.patient.forename = "LESLEY"
    bcds1.patient.address = ["24 HIGH STREET"]
    bcds1.patient.sex = 'F'
    bcds1.patient.nhs_number = '0000000000'
    bcds1.patient.date_of_birth = datetime.date(1967, 2, 7)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 1)

    # Treatments: "Ethnic Origin 7"
    bcds1.treatments = [
        treatments.ETHNIC_ORIGIN_7_OTHER_MIXED_BACKGROUND,
        treatments.DOMICILIARY_SERVICES,
    ]

    return bcds1


def from_model(bcds1, patient, episode):
    demographics = patient.demographics()
    demographics.surname = "CARLTON"
    demographics.first_name = "LESLEY"
    demographics.house_number_or_name = "24"
    demographics.street = "HIGH STREET"
    demographics.sex = "Female"
    demographics.date_of_birth = datetime.date(1967, 2, 7)
    demographics.ethnicity = "Other mixed background"
    demographics.save()

    episode.fp17otherdentalservices_set.update(
        domicillary_services=True
    )

    episode.fp17incompletetreatment_set.update(
        date_of_acceptance=datetime.date(2017, 4, 1),
        completion_or_last_visit=datetime.date(2017, 4, 1)
    )
    translate_to_bdcs1(bcds1, episode)
