import datetime

from fp17 import treatments
from odonto import models
from odonto.odonto_submissions.serializers import translate_to_bdcs1


def annotate(bcds1):
    bcds1.patient.surname = "BEARLEY"
    bcds1.patient.forename = "LANCE"
    bcds1.patient.address = ["4 HIGH STREET"]
    bcds1.patient.sex = 'M'
    bcds1.patient.nhs_number = '0000000000'
    bcds1.patient.date_of_birth = datetime.date(1959, 4, 5)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 1)

    bcds1.patient_charge_pence = 2060

    # Treatments: "Antibiotic Items (9318 1), Decayed Permanent 0, Missing
    # Permanent 1, Filled Permanent 12, Ethnic Origin 4"
    bcds1.treatments = [
        treatments.TREATMENT_CATEGORY_URGENT,
        treatments.ANTIBIOTIC_ITEMS(1),
        treatments.MISSING_PERMANENT(1),
        treatments.FILLED_PERMANENT(12),
        treatments.ETHNIC_ORIGIN_4_WHITE_AND_BLACK_CARIBBEAN,
    ]

    return bcds1


def from_model(bcds1, patient, episode):
    demographics = patient.demographics()
    demographics.surname = "BEARLEY"
    demographics.first_name = "LANCE"
    demographics.house_number_or_name = "4"
    demographics.street = "HIGH STREET"
    demographics.sex = "Male"
    demographics.date_of_birth = datetime.date(1959, 4, 5)
    demographics.ethnicity = "White and black caribbean"
    demographics.save()

    episode.fp17treatmentcategory_set.update(
        treatment_category=models.Fp17TreatmentCategory.URGENT_TREATMENT
    )

    episode.fp17clinicaldataset_set.update(
        antibiotic_items_prescribed=1,
        decayed_teeth_permanent=0,
        missing_teeth_permanent=1,
        filled_teeth_permanent=12,
    )

    episode.fp17exemptions_set.update(
        patient_charge_collected="20.60"
    )

    episode.fp17incompletetreatment_set.update(
        date_of_acceptance=datetime.date(2017, 4, 1),
        completion_or_last_visit=datetime.date(2017, 4, 1)
    )

    translate_to_bdcs1(bcds1, episode)
