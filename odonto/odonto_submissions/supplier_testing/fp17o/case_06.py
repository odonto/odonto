"""
Tests the Covid status serialization
"""
import datetime
from django.conf import settings
from odonto.odonto_submissions.serializers import translate_to_bdcs1
from odonto import models
from fp17 import treatments


def annotate(bcds1):
    bcds1.patient.surname = "IBSTOCK"
    bcds1.patient.forename = "WILLIAM"
    bcds1.patient.address = ["35 HIGH STREET"]
    bcds1.patient.sex = 'M'
    bcds1.patient.nhs_number = '0000000000'
    bcds1.patient.date_of_birth = datetime.date(2005, 1, 24)

    bcds1.date_of_acceptance = datetime.date(2019, 10, 9)
    bcds1.date_of_completion = datetime.date(2019, 10, 12)

    bcds1.treatments = [
        treatments.ASSESS_AND_REVIEW,
        treatments.DAY_OF_REFERRAL(9),
        treatments.MONTH_OF_REFERRAL(10),
        treatments.YEAR_OF_REFERRAL(19),
        treatments.ETHNIC_ORIGIN_PATIENT_DECLINED,

    ]

    if settings.ALWAYS_DECLINE_EMAIL_PHONE:
        bcds1.treatments.extend([
            treatments.EMAIL_DECLINED,
            treatments.PHONE_NUMBER_DECLINED
        ])

    return bcds1


def from_model(bcds1, patient, episode):
    demographics = patient.demographics()
    demographics.surname = "IBSTOCK"
    demographics.first_name = "WILLIAM"
    demographics.house_number_or_name = "35"
    demographics.street = "HIGH STREET"
    demographics.sex = "Male"
    demographics.ethnicity = "Patient declined"
    demographics.date_of_birth = datetime.date(2005, 1, 24)
    demographics.save()

    episode.orthodonticassessment_set.update(
        assessment=models.OrthodonticAssessment.ASSESSMENT_AND_REVIEW,
        date_of_referral=datetime.date(2019, 10, 9),
        date_of_assessment=datetime.date(2019, 10, 9),
    )

    episode.orthodontictreatment_set.update(
        date_of_completion=datetime.date(2019, 10, 12),
    )

    translate_to_bdcs1(bcds1, episode)
