import datetime
from odonto import models
from odonto.odonto_submissions.serializers import translate_to_bdcs1
from fp17 import treatments


def annotate(bcds1):
    bcds1.patient.surname = "CANLEY"
    bcds1.patient.forename = "VIOLET"
    bcds1.patient.address = ["22 HIGH STREET"]
    bcds1.patient.sex = 'F'
    bcds1.patient.nhs_number = '0000000000'
    bcds1.patient.date_of_birth = datetime.date(1929, 5, 25)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 1)

    # Treatments: "Filled Permanent 3, Ethnic Origin 5"
    bcds1.treatments = [
        treatments.REMOVAL_OF_SUTURES,
        treatments.FILLED_PERMANENT(3),
        treatments.ETHNIC_ORIGIN_5_WHITE_AND_BLACK_AFRICAN,
    ]

    return bcds1


def from_model(bcds1, patient, episode):
    demographics = patient.demographics()
    demographics.surname = "CANLEY"
    demographics.first_name = "VIOLET"
    demographics.house_number_or_name = "22"
    demographics.street = "HIGH STREET"
    demographics.sex = "Female"
    demographics.date_of_birth = datetime.date(1929, 5, 25)
    demographics.ethnicity = "White and black african"
    demographics.save()

    episode.fp17treatmentcategory_set.update(
        treatment_category=models.Fp17TreatmentCategory.REMOVAL_OF_SUTURES
    )

    episode.fp17clinicaldataset_set.update(
        filled_teeth_permanent=3
    )

    episode.fp17incompletetreatment_set.update(
        date_of_acceptance=datetime.date(2017, 4, 1),
        completion_or_last_visit=datetime.date(2017, 4, 1)
    )
    translate_to_bdcs1(bcds1, episode)
