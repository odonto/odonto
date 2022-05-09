import datetime
from odonto.odonto_submissions.serializers import translate_to_bdcs1
from fp17 import treatments


def annotate(bcds1):
    bcds1.patient.surname = "ALBRIGHTON"
    bcds1.patient.forename = "GARY"
    bcds1.patient.address = ["29 HIGH STREET"]
    bcds1.patient.sex = 'M'
    bcds1.patient.nhs_number = '0000000000'
    bcds1.patient.date_of_birth = datetime.date(1966, 10, 30)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 1)

    bcds1.patient_charge_pence = 5630

    # Treatments: "Examination (9317), Extractions x 1, Recall Interval (9172
    # 9), Ethnic Origin 13 "
    bcds1.treatments = [
        treatments.TREATMENT_CATEGORY(2),
        treatments.EXTRACTION(1),
        treatments.RECALL_INTERVAL(9),
        treatments.ETHNIC_ORIGIN_13_BLACK_OR_BLACK_BRITISH_AFRICAN,
    ]

    return bcds1


def from_model(bcds1, patient, episode):
    demographics = patient.demographics()
    demographics.surname = "ALBRIGHTON"
    demographics.first_name = "GARY"
    demographics.house_number_or_name = "29"
    demographics.street = "HIGH STREET"
    demographics.sex = "Male"
    demographics.date_of_birth = datetime.date(1966, 10, 30)
    demographics.ethnicity = "Black or black british african"
    demographics.save()

    episode.fp17exemptions_set.update(
        patient_charge_collected=56.30
    )
    episode.fp17treatmentcategory_set.update(
        treatment_category="Band 2",
    )
    episode.fp17recall_set.update(
        number_of_months=9
    )
    episode.fp17clinicaldataset_set.update(
        extractions=1
    )

    episode.fp17incompletetreatment_set.update(
        date_of_acceptance=datetime.date(2017, 4, 1),
        completion_or_last_visit=datetime.date(2017, 4, 1)
    )

    translate_to_bdcs1(bcds1, episode)
