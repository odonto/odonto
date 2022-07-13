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

    bcds1.date_of_acceptance = datetime.date(2017, 5, 1)
    bcds1.date_of_completion = datetime.date(2017, 5, 1)

    # Treatments: "Other Treatment (9399), Ethnic Origin 13"
    bcds1.treatments = [
        treatments.TREATMENT_CATEGORY(1),
        treatments.OTHER_TREATMENT,
        treatments.ETHNIC_ORIGIN_13_BLACK_OR_BLACK_BRITISH_AFRICAN,

        # "Further treatment within 2 months" service
        treatments.FURTHER_TREATMENT_WITHIN_TWO_MONTHS
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

    episode.fp17treatmentcategory_set.update(
        treatment_category="Band 1",
    )

    episode.fp17clinicaldataset_set.update(
        other_treatment=True
    )

    episode.fp17otherdentalservices_set.update(
        further_treatment_within_2_months=True
    )

    episode.fp17incompletetreatment_set.update(
        date_of_acceptance=datetime.date(2017, 5, 1),
        completion_or_last_visit=datetime.date(2017, 5, 1)
    )

    translate_to_bdcs1(bcds1, episode)
