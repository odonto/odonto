import datetime
from odonto.odonto_submissions.serializers import translate_to_bdcs1
from fp17 import treatments


def annotate(bcds1):
    bcds1.patient.surname = "HADFIELD"
    bcds1.patient.forename = "DAVID"
    bcds1.patient.address = ["26 HIGH STREET"]
    bcds1.patient.sex = 'M'
    bcds1.patient.nhs_number = '0000000000'
    bcds1.patient.date_of_birth = datetime.date(1967, 5, 14)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 1)

    bcds1.patient_charge_pence = 5630

    # Treatments: "Examination (9317), Radiographs x 4,  Bridges x 2,
    # Antibiotic Items (9318 1), Recall Interval (9172 6), Ethnic Origin 9"
    bcds1.treatments = [
        treatments.TREATMENT_CATEGORY(3),
        treatments.RADIOGRAPHS(4),
        treatments.BRIDGES_FITTED(2),
        treatments.ANTIBIOTIC_ITEMS(1),
        treatments.RECALL_INTERVAL(6),
        treatments.ETHNIC_ORIGIN_9_ASIAN_OR_ASIAN_BRITISH_PAKISTANI,
    ]

    return bcds1


def from_model(bcds1, patient, episode):
    demographics = patient.demographics()
    demographics.surname = "HADFIELD"
    demographics.first_name = "DAVID"
    demographics.house_number_or_name = "26"
    demographics.street = "HIGH STREET"
    demographics.sex = "Male"
    demographics.date_of_birth = datetime.date(1967, 5, 14)
    demographics.ethnicity = "Asian or asian british pakistani"
    demographics.save()

    episode.fp17exemptions_set.update(
        patient_charge_collected=56.30
    )
    episode.fp17treatmentcategory_set.update(
        treatment_category="Band 3",
    )
    episode.fp17recall_set.update(
        number_of_months=6
    )
    episode.fp17clinicaldataset_set.update(
        radiographs_taken=4,
        bridges_fitted=2,
        antibiotic_items_prescribed=1
    )
    episode.fp17incompletetreatment_set.update(
        date_of_acceptance=datetime.date(2017, 4, 1),
        completion_or_last_visit=datetime.date(2017, 4, 1)
    )
    translate_to_bdcs1(bcds1, episode)
