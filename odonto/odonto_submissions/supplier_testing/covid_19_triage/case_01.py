import datetime
from django.conf import settings
from odonto.odonto_submissions.serializers import translate_to_bdcs1
from odonto.models import CovidTriage

from fp17 import treatments


def annotate(bcds1):
    bcds1.contract_number = settings.FP17_CONTRACT_NUMBER
    bcds1.patient.surname = "BARLASTON"
    bcds1.patient.forename = "SALLY"
    bcds1.patient.address = ["1 HIGH STREET"]
    bcds1.patient.sex = 'F'
    bcds1.patient.nhs_number = '0000000000'
    bcds1.patient.date_of_birth = datetime.date(1958, 1, 23)

    bcds1.date_of_acceptance = datetime.date(2020, 3, 1)
    bcds1.date_of_completion = datetime.date(2020, 3, 1)

    # Treatments: "Examination (9317), Recall Interval (9172 9), Scale &
    # Polish, Ethnic Origin 1"
    bcds1.treatments = [
        treatments.TREATMENT_CATEGORY(6),
        treatments.PATIENT_GROUP(2),
        treatments.HOUR_OF_CONTACT(14),
        treatments.MINUTE_OF_CONTACT(10),
        treatments.PRIMARY_REASON(7)
    ]

    return bcds1


def from_model(bcds1, patient, episode):
    demographics = patient.demographics()
    demographics.surname = "Barlaston"
    demographics.first_name = "Sally"
    demographics.house_number_or_name = "1"
    demographics.street = "HIGH STREET"
    demographics.sex = "Female"
    demographics.date_of_birth = datetime.date(1958, 1, 23)
    demographics.ethnicity = "White british"
    demographics.save()
    episode.covidtriage_set.update(
        covid_status="Increased risk of illness from COVID-19",
        datetime_of_contact=datetime.datetime(2020, 3, 1, 14, 10),
        triage_type=CovidTriage.FP17,
        primary_reason="Routine treatment"
    )
    translate_to_bdcs1(bcds1, episode)
