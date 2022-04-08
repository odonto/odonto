import datetime
from odonto import models
from odonto.odonto_submissions.serializers import translate_to_bdcs1
from fp17 import treatments, exemptions


def annotate(bcds1):
    bcds1.patient.surname = "BUTTON"
    bcds1.patient.forename = "ROY"
    bcds1.patient.address = ["35 HIGH STREET"]
    bcds1.patient.sex = 'M'
    bcds1.patient.nhs_number = '0000000000'
    bcds1.patient.date_of_birth = datetime.date(1964, 10, 17)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 1)

    # "Tax Credits (No Evidence Seen)"
    bcds1.exemption_remission = {
        'code': exemptions.PENSION_CREDIT_GUARANTEE_CREDIT.NO_EVIDENCE_SEEN,
    }

    # Treatments: "None"
    bcds1.treatments = [
        # 'Band 4'
        treatments.TREATMENT_CATEGORY_URGENT,
        treatments.ETHNIC_ORIGIN_PATIENT_DECLINED,
    ]

    return bcds1


def from_model(bcds1, patient, episode):
    demographics = patient.demographics()
    demographics.surname = "BUTTON"
    demographics.first_name = "ROY"
    demographics.house_number_or_name = "35"
    demographics.street = "HIGH STREET"
    demographics.sex = "Male"
    demographics.ethnicity = "Patient declined"
    demographics.date_of_birth = datetime.date(1964, 10, 17)
    demographics.save()

    episode.fp17treatmentcategory_set.update(
        treatment_category=models.Fp17TreatmentCategory.URGENT_TREATMENT
    )

    episode.fp17exemptions_set.update(
        pension_credit_guarantee_credit=True,
        evidence_of_exception_or_remission_seen=False
    )

    episode.fp17incompletetreatment_set.update(
        date_of_acceptance=datetime.date(2017, 4, 1),
        completion_or_last_visit=datetime.date(2017, 4, 1)
    )
    translate_to_bdcs1(bcds1, episode)
