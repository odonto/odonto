"""
Tests the Covid status serialization
"""
import datetime
from odonto.odonto_submissions.serializers import translate_to_bdcs1
from fp17 import treatments


def annotate(bcds1):
    bcds1.patient.surname = "HATTON"
    bcds1.patient.forename = "TONY"
    bcds1.patient.address = ["34 HIGH STREET"]
    bcds1.patient.sex = 'M'
    bcds1.patient.nhs_number = '0000000000'
    bcds1.patient.date_of_birth = datetime.date(1970, 1, 31)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 5, 1)

    bcds1.treatments = [
        treatments.ETHNIC_ORIGIN_PATIENT_DECLINED,
        treatments.SHIELDING_PATIENT(1),
        treatments.INCREASED_RISK(2),
    ]

    return bcds1


def from_model(bcds1, patient, episode):
    demographics = patient.demographics()
    demographics.surname = "HATTON"
    demographics.first_name = "TONY"
    demographics.house_number_or_name = "34"
    demographics.street = "HIGH STREET"
    demographics.sex = "Male"
    demographics.ethnicity = "Patient declined"
    demographics.date_of_birth = datetime.date(1970, 1, 31)
    demographics.save()

    episode.fp17incompletetreatment_set.update(
        date_of_acceptance=datetime.date(2017, 4, 1),
        completion_or_last_visit=datetime.date(2017, 5, 1)
    )

    status = episode.covidstatus_set.get()
    status.shielding_patient = 1
    status.increased_risk = 2
    status.save()

    translate_to_bdcs1(bcds1, episode)
