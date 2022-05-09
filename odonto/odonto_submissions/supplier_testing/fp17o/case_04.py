import datetime
from django.conf import settings
from odonto.odonto_submissions.serializers import translate_to_bdcs1
from odonto import models
from fp17 import treatments, exemptions


def annotate(bcds1):
    bcds1.patient.surname = "IBSTOCK"
    bcds1.patient.forename = "WILLIAM"
    bcds1.patient.address = ["35 HIGH STREET"]
    bcds1.patient.sex = 'M'
    bcds1.patient.nhs_number = '0000000000'
    bcds1.patient.date_of_birth = datetime.date(2004, 10, 15)

    bcds1.date_of_acceptance = datetime.date(2019, 10, 12)

    bcds1.exemption_remission = {
        'code': exemptions.PATIENT_UNDER_18.EVIDENCE_SEEN,
    }

    bcds1.treatments = [
        treatments.ETHNIC_ORIGIN_PATIENT_DECLINED,
        treatments.ASSESS_AND_APPLIANCE_FITTED,
        treatments.PROPOSED_TREATMENT,
        treatments.DAY_OF_REFERRAL(11),
        treatments.MONTH_OF_REFERRAL(10),
        treatments.YEAR_OF_REFERRAL(19),
        treatments.DAY_APPLIANCE_FITTED(3),
        treatments.MONTH_APPLIANCE_FITTED(11),
        treatments.YEAR_APPLIANCE_FITTED(19),
        treatments.IOTN(4),
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
    demographics.date_of_birth = datetime.date(2004, 10, 15)
    demographics.save()

    episode.fp17exemptions_set.update(
        patient_under_18=True,
        evidence_of_exception_or_remission_seen=True
    )

    date_of_referral = datetime.date(2019, 10, 11)
    date_of_assessment = datetime.date(2019, 10, 12)
    date_appliance_fitted = datetime.date(2019, 11, 3)
    episode.orthodonticassessment_set.update(
        date_of_referral=date_of_referral,
        date_of_assessment=date_of_assessment,
        date_of_appliance_fitted=date_appliance_fitted,
        assessment=models.OrthodonticAssessment.ASSESS_AND_APPLIANCE_FITTED,
        iotn="4"
    )
    translate_to_bdcs1(bcds1, episode)
