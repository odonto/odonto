import datetime
from odonto.odonto_submissions.serializers import translate_to_bdcs1
from fp17 import treatments, exemptions


def annotate(bcds1):
    bcds1.patient.surname = "CAMPBELL"
    bcds1.patient.forename = "PAUL"
    bcds1.patient.address = ["39 HIGH STREET"]
    bcds1.patient.sex = 'M'
    bcds1.patient.nhs_number = '0000000000'
    bcds1.patient.date_of_birth = datetime.date(1970, 9, 1)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 1)

    # "Employment Support Allowance"
    bcds1.exemption_remission = {
        'code': exemptions.INCOME_RELATED_EMPLOYMENT_AND_SUPPORT_ALLOWANCE.EVIDENCE_SEEN,
    }

    # Treatments: "Extraction 1"
    bcds1.treatments = [
        treatments.TREATMENT_CATEGORY(2),
        treatments.ETHNIC_ORIGIN_PATIENT_DECLINED,
    ]

    return bcds1


def from_model(bcds1, patient, episode):
    demographics = patient.demographics()
    demographics.surname = "CAMPBELL"
    demographics.first_name = "PAUL"
    demographics.house_number_or_name = "39"
    demographics.street = "HIGH STREET"
    demographics.sex = "Male"
    demographics.ethnicity = "Patient declined"
    demographics.date_of_birth = datetime.date(1970, 9, 1)
    demographics.save()

    episode.fp17treatmentcategory_set.update(
        treatment_category="Band 2",
    )

    episode.fp17exemptions_set.update(
        income_related_employment_and_support_allowance=True,
        evidence_of_exception_or_remission_seen=True
    )

    episode.fp17incompletetreatment_set.update(
        date_of_acceptance=datetime.date(2017, 4, 1),
        completion_or_last_visit=datetime.date(2017, 4, 1)
    )

    translate_to_bdcs1(bcds1, episode)
