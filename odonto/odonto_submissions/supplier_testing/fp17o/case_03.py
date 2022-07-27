import datetime
from django.conf import settings
from odonto import models
from odonto.odonto_submissions.serializers import translate_to_bdcs1
from fp17 import treatments, exemptions


def annotate(bcds1):
    bcds1.patient.surname = "IBSTOCK"
    bcds1.patient.forename = "WILLIAM"
    bcds1.patient.address = ["35 HIGH STREET"]
    bcds1.patient.sex = 'M'
    bcds1.patient.nhs_number = '0000000000'
    bcds1.patient.date_of_birth = datetime.date(2005, 1, 24)

    bcds1.date_of_acceptance = datetime.date(2019, 10, 12)
    bcds1.date_of_completion = datetime.date(2019, 10, 12)

    bcds1.exemption_remission = {
        'code': exemptions.PATIENT_UNDER_18.EVIDENCE_SEEN,
    }

    bcds1.treatments = [
        treatments.ETHNIC_ORIGIN_PATIENT_DECLINED,
        treatments.TREATMENT_ABANDONED,
        treatments.COMPLETED_TREATMENT,
        treatments.PATIENT_FAILED_TO_RETURN,
        treatments.RADIOGRAPHS(1),
        treatments.FIXED_UPPER_APPLIANCE,
        treatments.IOTN(0),
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

    episode.fp17exemptions_set.update(
        patient_under_18=True,
        evidence_of_exception_or_remission_seen=True
    )
    episode.orthodonticdataset_set.update(
        fixed_upper_appliance=True,
        radiograph=1
    )

    episode.orthodontictreatment_set.update(
        completion_type=models.OrthodonticTreatment.PATIENT_FAILED_TO_RETURN,
        date_of_completion=datetime.date(2019, 10, 12),
        iotn=models.OrthodonticTreatment.IOTN_NOT_APPLICABLE
    )

    translate_to_bdcs1(bcds1, episode)
