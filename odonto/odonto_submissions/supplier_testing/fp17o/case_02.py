import datetime
from odonto.odonto_submissions.serializers import translate_to_bdcs1
from odonto import models
from fp17 import treatments, exemptions


def annotate(bcds1):
    bcds1.patient.surname = "IBSTOCK"
    bcds1.patient.forename = "WILLIAM"
    bcds1.patient.address = ["35 HIGH STREET"]
    bcds1.patient.sex = 'M'
    bcds1.patient.nhs_number = '0000000000'
    bcds1.patient.date_of_birth = datetime.date(2006, 10, 15)

    bcds1.date_of_acceptance = datetime.date(2019, 10, 12)
    bcds1.date_of_completion = datetime.date(2019, 10, 12)

    bcds1.exemption_remission = {
        'code': exemptions.PATIENT_UNDER_18.EVIDENCE_SEEN
    }

    bcds1.treatments = [
        treatments.COMPLETED_TREATMENT,
        treatments.EMAIL_DECLINED,
        treatments.PHONE_NUMBER_DECLINED,
        treatments.ETHNIC_ORIGIN_PATIENT_DECLINED,
        treatments.REMOVABLE_UPPER_APPLIANCE,
        treatments.FIXED_UPPER_APPLIANCE,
        treatments.FIXED_LOWER_APPLIANCE,
        treatments.RETAINER_LOWER,
        treatments.RETAINER_UPPER,
        treatments.TREATMENT_COMPLETED,
        treatments.PAR_SCORES_CALCULATED,
        treatments.DAY_OF_REFERRAL(9),
        treatments.MONTH_OF_REFERRAL(10),
        treatments.YEAR_OF_REFERRAL(19),
        treatments.IOTN(2),
        treatments.ASSESS_AND_REVIEW
    ]

    return bcds1


def from_model(bcds1, patient, episode):
    demographics = patient.demographics()
    demographics.surname = "IBSTOCK"
    demographics.first_name = "WILLIAM"
    demographics.house_number_or_name = "35"
    demographics.street = "HIGH STREET"
    demographics.sex = "Male"
    demographics.ethnicity = "Patient declined"
    demographics.date_of_birth = datetime.date(2006, 10, 15)
    demographics.patient_declined_phone = True
    demographics.patient_declined_email = True
    demographics.save()

    episode.fp17exemptions_set.update(
        patient_under_18=True,
        evidence_of_exception_or_remission_seen=True
    )

    episode.orthodonticdataset_set.update(
        treatment_type=models.OrthodonticDataSet.COMPLETED,
        removable_upper_appliance=True,
        fixed_upper_appliance=True,
        fixed_lower_appliance=True,
        retainer_upper=True,
        retainer_lower=True
    )

    episode.orthodontictreatment_set.update(
        completion_type=models.OrthodonticTreatment.TREATMENT_COMPLETED,
        par_scores_calculated=True,
        date_of_completion=datetime.date(2019, 10, 12),
        iotn="2"
    )

    episode.orthodonticassessment_set.update(
        assessment=models.OrthodonticAssessment.ASSESSMENT_AND_REVIEW,
        date_of_assessment=datetime.date(2019, 10, 11),
        date_of_referral=datetime.date(2019, 10, 9),
    )

    translate_to_bdcs1(bcds1, episode)
