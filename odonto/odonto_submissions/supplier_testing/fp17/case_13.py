import datetime
from odonto.odonto_submissions.serializers import translate_to_bdcs1
from fp17 import treatments


def annotate(bcds1):
    bcds1.patient.surname = "BOTTESFORD"
    bcds1.patient.forename = "JULIAN"
    bcds1.patient.address = ["13 HIGH STREET"]
    bcds1.patient.sex = 'M'
    bcds1.patient.nhs_number = '0000000000'
    bcds1.patient.date_of_birth = datetime.date(1950, 2, 14)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 1)

    bcds1.patient_charge_pence = 2060

    # Treatments: "Examination (9317), Ethnic Origin 13"
    bcds1.treatments = [
        treatments.TREATMENT_CATEGORY(1),
        treatments.EXAMINATION,
        treatments.ETHNIC_ORIGIN_13_BLACK_OR_BLACK_BRITISH_AFRICAN,
    ]

    return bcds1


def from_model(bcds1, patient, episode):
    demographics = patient.demographics()
    demographics.surname = "BOTTESFORD"
    demographics.first_name = "JULIAN"
    demographics.house_number_or_name = "13"
    demographics.street = "HIGH STREET"
    demographics.sex = "Male"
    demographics.date_of_birth = datetime.date(1950, 2, 14)
    demographics.ethnicity = "Black or black british african"
    demographics.save()

    episode.fp17treatmentcategory_set.update(
        treatment_category="Band 1"
    )

    episode.fp17clinicaldataset_set.update(
        examination=True
    )

    episode.fp17exemptions_set.update(
        patient_charge_collected="20.60"
    )

    episode.fp17incompletetreatment_set.update(
        date_of_acceptance=datetime.date(2017, 4, 1),
        completion_or_last_visit=datetime.date(2017, 4, 1)
    )
    translate_to_bdcs1(bcds1, episode)
