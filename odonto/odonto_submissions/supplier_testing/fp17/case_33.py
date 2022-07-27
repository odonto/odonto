import datetime
from odonto.odonto_submissions.serializers import translate_to_bdcs1
from fp17 import treatments


def annotate(bcds1):
    bcds1.patient.surname = "ALSAGER"
    bcds1.patient.forename = "SAM"
    bcds1.patient.address = ["31 HIGH STREET"]
    bcds1.patient.sex = 'F'
    bcds1.patient.nhs_number = '0000000000'
    bcds1.patient.date_of_birth = datetime.date(1947, 8, 16)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 1)

    bcds1.patient_charge_pence = 5630

    # Treatments: "Fillings x 2, Scale and Polish, Radiographs x 2, Examination
    # (9317), Antibiotic Items Prescribed (9318 x 1), Other Treatment (9399),
    # Recall Interval (9172 18), Ethnic Origin 1, Best Practice Prevention"
    bcds1.treatments = [
        treatments.TREATMENT_CATEGORY(2),
        treatments.PERMANENT_FILLINGS(2),
        treatments.SCALE_AND_POLISH,
        treatments.RADIOGRAPHS(2),
        treatments.EXAMINATION,
        treatments.ANTIBIOTIC_ITEMS(1),
        treatments.OTHER_TREATMENT,
        treatments.RECALL_INTERVAL(18),
        treatments.ETHNIC_ORIGIN_1_WHITE_BRITISH,
        treatments.BEST_PRACTICE_PREVENTION,
    ]

    return bcds1


def from_model(bcds1, patient, episode):
    demographics = patient.demographics()
    demographics.surname = "ALSAGER"
    demographics.first_name = "SAM"
    demographics.house_number_or_name = "31"
    demographics.street = "HIGH STREET"
    demographics.sex = "Female"
    demographics.date_of_birth = datetime.date(1947, 8, 16)
    demographics.ethnicity = "White british"
    demographics.save()

    episode.fp17treatmentcategory_set.update(
        treatment_category="Band 2",
    )

    episode.fp17clinicaldataset_set.update(
        permanent_fillings=2,
        scale_and_polish=True,
        radiographs_taken=2,
        examination=1,
        antibiotic_items_prescribed=1,
        other_treatment=True,
        best_practice_prevention=True
    )

    episode.fp17recall_set.update(
        number_of_months=18
    )

    episode.fp17exemptions_set.update(
        patient_charge_collected=56.30
    )

    episode.fp17incompletetreatment_set.update(
        date_of_acceptance=datetime.date(2017, 4, 1),
        completion_or_last_visit=datetime.date(2017, 4, 1)
    )
    translate_to_bdcs1(bcds1, episode)
