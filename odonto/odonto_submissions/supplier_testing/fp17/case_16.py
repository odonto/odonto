import datetime
from odonto import models
from odonto.odonto_submissions.serializers import translate_to_bdcs1
from fp17 import treatments


def annotate(bcds1):
    bcds1.patient.surname = "BROOME"
    bcds1.patient.forename = "RON"
    bcds1.patient.address = ["16 HIGH STREET"]
    bcds1.patient.sex = 'M'
    bcds1.patient.nhs_number = '0000000000'
    bcds1.patient.date_of_birth = datetime.date(1935, 4, 29)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 1)

    bcds1.patient_charge_pence = 2060

    # Treatments: "Filling x 1, Antibiotic items prescribed (9318 1), Ethnic
    # Origin 16"
    bcds1.treatments = [
        treatments.TREATMENT_CATEGORY_URGENT,
        treatments.ANTIBIOTIC_ITEMS(1),
        treatments.ETHNIC_ORIGIN_ANY_OTHER_ETHNIC_GROUP,
    ]

    return bcds1


def from_model(bcds1, patient, episode):
    demographics = patient.demographics()
    demographics.surname = "BROOME"
    demographics.first_name = "RON"
    demographics.house_number_or_name = "16"
    demographics.street = "HIGH STREET"
    demographics.sex = "Male"
    demographics.date_of_birth = datetime.date(1935, 4, 29)
    demographics.ethnicity = "Other ethnic group"
    demographics.save()

    episode.fp17exemptions_set.update(
        patient_charge_collected="20.60"
    )

    episode.fp17treatmentcategory_set.update(
        treatment_category=models.Fp17TreatmentCategory.URGENT_TREATMENT
    )

    episode.fp17clinicaldataset_set.update(
        antibiotic_items_prescribed=1
    )
    episode.fp17incompletetreatment_set.update(
        date_of_acceptance=datetime.date(2017, 4, 1),
        completion_or_last_visit=datetime.date(2017, 4, 1)
    )
    translate_to_bdcs1(bcds1, episode)
