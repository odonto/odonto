import datetime

from fp17 import treatments
from odonto import models
from odonto.odonto_submissions.serializers import translate_to_bdcs1


def annotate(bcds1):
    bcds1.patient.surname = "BEESTON"
    bcds1.patient.forename = "TODD"
    bcds1.patient.address = ["6 HIGH STREET"]
    bcds1.patient.sex = 'M'
    bcds1.patient.nhs_number = '0000000000'
    bcds1.patient.date_of_birth = datetime.date(1956, 12, 3)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 1)

    # Treatments: "Antibiotic items (9318 1), Ethnic Origin 6"
    bcds1.treatments = [
        treatments.PRESCRIPTION,
        treatments.ANTIBIOTIC_ITEMS(1),
        treatments.ETHNIC_ORIGIN_6_WHITE_AND_ASIAN,
    ]

    return bcds1


def from_model(bcds1, patient, episode):
    demographics = patient.demographics()
    demographics.surname = "BEESTON"
    demographics.first_name = "TODD"
    demographics.house_number_or_name = "6"
    demographics.street = "HIGH STREET"
    demographics.sex = "Male"
    demographics.date_of_birth = datetime.date(1956, 12, 3)
    demographics.ethnicity = "White and asian"
    demographics.save()
    episode.fp17treatmentcategory_set.update(
        treatment_category=models.Fp17TreatmentCategory.PRESCRIPTION_ONLY
    )

    episode.fp17clinicaldataset_set.update(
        antibiotic_items_prescribed=1
    )

    episode.fp17incompletetreatment_set.update(
        date_of_acceptance=datetime.date(2017, 4, 1),
        completion_or_last_visit=datetime.date(2017, 4, 1)
    )
    translate_to_bdcs1(bcds1, episode)
