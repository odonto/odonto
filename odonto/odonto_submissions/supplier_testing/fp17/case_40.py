import datetime
from odonto import models
from odonto.odonto_submissions.serializers import translate_to_bdcs1
from fp17 import treatments, exemptions


def annotate(bcds1):
    bcds1.patient.surname = "BYRON"
    bcds1.patient.forename = "HENRY"
    bcds1.patient.address = ["37 HIGH STREET"]
    bcds1.patient.sex = 'M'
    bcds1.patient.nhs_number = '0000000000'
    bcds1.patient.date_of_birth = datetime.date(1948, 3, 17)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 1)

    # "Pension Credits"
    bcds1.exemption_remission = {
        'code': exemptions.PENSION_CREDIT_GUARANTEE_CREDIT.EVIDENCE_SEEN,
    }

    # Treatments: "Filling 1"
    bcds1.treatments = [
        treatments.PERMANENT_FILLINGS(1),
        treatments.ETHNIC_ORIGIN_PATIENT_DECLINED,

        # 'Band 4'
        treatments.TREATMENT_CATEGORY_URGENT,
    ]

    return bcds1


def from_model(bcds1, patient, episode):
    demographics = patient.demographics()
    demographics.surname = "BYRON"
    demographics.first_name = "HENRY"
    demographics.house_number_or_name = "37"
    demographics.street = "HIGH STREET"
    demographics.sex = "Male"
    demographics.ethnicity = "Patient declined"
    demographics.date_of_birth = datetime.date(1948, 3, 17)
    demographics.save()

    episode.fp17treatmentcategory_set.update(
        treatment_category=models.Fp17TreatmentCategory.URGENT_TREATMENT
    )

    episode.fp17exemptions_set.update(
        pension_credit_guarantee_credit=True,
        evidence_of_exception_or_remission_seen=True
    )

    episode.fp17clinicaldataset_set.update(
        permanent_fillings=1
    )

    episode.fp17incompletetreatment_set.update(
        date_of_acceptance=datetime.date(2017, 4, 1),
        completion_or_last_visit=datetime.date(2017, 4, 1)
    )
    translate_to_bdcs1(bcds1, episode)
