import datetime
from fp17 import treatments
from odonto import models
from odonto.odonto_submissions.serializers import translate_to_bdcs1


def annotate(bcds1):
    bcds1.patient.surname = "BERKSWELL"
    bcds1.patient.forename = "KEITH"
    bcds1.patient.address = ["8 HIGH STREET"]
    bcds1.patient.sex = 'M'
    bcds1.patient.nhs_number = '0000000000'
    bcds1.patient.date_of_birth = datetime.date(1947, 5, 5)

    bcds1.date_of_acceptance = datetime.date(2020, 4, 1)
    bcds1.date_of_completion = datetime.date(2020, 4, 2)

    # Treatments: "Ethnic Origin 8, Missing Permanent 0"
    bcds1.treatments = [
        treatments.BRIDGE_REPAIRS,
        treatments.ETHNIC_ORIGIN_8_ASIAN_OR_ASIAN_BRITISH_INDIAN,
        treatments.AEROSOL_GENERATING_PROCEDURE(2)
    ]

    return bcds1


def from_model(bcds1, patient, episode):
    demographics = patient.demographics()
    demographics.surname = "BERKSWELL"
    demographics.first_name = "KEITH"
    demographics.house_number_or_name = "8"
    demographics.street = "HIGH STREET"
    demographics.sex = "Male"
    demographics.date_of_birth = datetime.date(1947, 5, 5)
    demographics.ethnicity = "Asian or asian british indian"
    demographics.save()

    episode.fp17treatmentcategory_set.update(
        treatment_category=models.Fp17TreatmentCategory.BRIDGE_REPAIRS
    )

    episode.fp17clinicaldataset_set.update(
        missing_teeth_permanent=0,
        aerosol_generating_procedures=2
    )

    episode.fp17incompletetreatment_set.update(
        date_of_acceptance=datetime.date(2020, 4, 1),
        completion_or_last_visit=datetime.date(2020, 4, 2)
    )
    translate_to_bdcs1(bcds1, episode)
