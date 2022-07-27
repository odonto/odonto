import datetime
from odonto import models
from odonto.odonto_submissions.serializers import translate_to_bdcs1
from fp17 import treatments, exemptions


def annotate(bcds1):
    bcds1.patient.surname = "BELPER"
    bcds1.patient.forename = "MATTHEW"
    bcds1.patient.address = ["7 HIGH STREET"]
    bcds1.patient.sex = 'M'
    bcds1.patient.nhs_number = '0000000000'
    bcds1.patient.date_of_birth = datetime.date(2003, 3, 26)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 1)

    # "Under 18"
    bcds1.exemption_remission = {
        'code': exemptions.PATIENT_UNDER_18.EVIDENCE_SEEN,
    }

    # Treatments: "Missing Deciduous 10, Ethnic Origin 7"
    bcds1.treatments = [
        treatments.DENTURE_REPAIRS,
        treatments.MISSING_DECIDUOUS(10),
        treatments.ETHNIC_ORIGIN_7_OTHER_MIXED_BACKGROUND,
    ]

    return bcds1


def from_model(bcds1, patient, episode):
    demographics = patient.demographics()
    demographics.surname = "BELPER"
    demographics.first_name = "MATTHEW"
    demographics.house_number_or_name = "7"
    demographics.street = "HIGH STREET"
    demographics.sex = "Male"
    demographics.date_of_birth = datetime.date(2003, 3, 26)
    demographics.ethnicity = "Other mixed background"
    demographics.save()

    episode.fp17exemptions_set.update(
        patient_under_18=True,
        evidence_of_exception_or_remission_seen=True
    )

    episode.fp17treatmentcategory_set.update(
        treatment_category=models.Fp17TreatmentCategory.DENTURE_REPAIRS
    )

    episode.fp17clinicaldataset_set.update(
        missing_teeth_deciduous=10
    )

    episode.fp17incompletetreatment_set.update(
        date_of_acceptance=datetime.date(2017, 4, 1),
        completion_or_last_visit=datetime.date(2017, 4, 1)
    )
    translate_to_bdcs1(bcds1, episode)
