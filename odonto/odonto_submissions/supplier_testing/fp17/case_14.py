import datetime
from odonto.odonto_submissions.serializers import translate_to_bdcs1
from fp17 import treatments


def annotate(bcds1):
    bcds1.patient.surname = "BOURNEVILLE"
    bcds1.patient.forename = "RITA"
    bcds1.patient.address = ["14 HIGH STREET"]
    bcds1.patient.sex = 'F'
    bcds1.patient.nhs_number = '0000000000'
    bcds1.patient.date_of_birth = datetime.date(1940, 6, 5)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 12)

    bcds1.patient_charge_pence = 5630

    # Treatments: "Fluoride Varnish, Filling x 1, Ethnic Origin 14"
    bcds1.treatments = [
        treatments.TREATMENT_CATEGORY(2),
        treatments.PERMANENT_FILLINGS(1),
        treatments.ETHNIC_ORIGIN_14_OTHER_BLACK_BACKGROUND,
    ]

    return bcds1


def from_model(bcds1, patient, episode):
    demographics = patient.demographics()
    demographics.surname = "BOURNEVILLE"
    demographics.first_name = "RITA"
    demographics.house_number_or_name = "14"
    demographics.street = "HIGH STREET"
    demographics.sex = "Female"
    demographics.date_of_birth = datetime.date(1940, 6, 5)
    demographics.ethnicity = "Other black background"
    demographics.save()

    episode.fp17treatmentcategory_set.update(
        treatment_category="Band 2"
    )

    episode.fp17clinicaldataset_set.update(
        permanent_fillings=1,
    )

    episode.fp17exemptions_set.update(
        patient_charge_collected="56.30"
    )

    episode.fp17incompletetreatment_set.update(
        date_of_acceptance=datetime.date(2017, 4, 1),
        completion_or_last_visit=datetime.date(2017, 4, 12)
    )
    translate_to_bdcs1(bcds1, episode)
