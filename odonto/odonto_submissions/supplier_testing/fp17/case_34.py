import datetime
from odonto.odonto_submissions.serializers import translate_to_bdcs1
from fp17 import treatments


def annotate(bcds1):
    bcds1.patient.surname = "ALVERCHURCH"
    bcds1.patient.forename = "CARL"
    bcds1.patient.address = ["31 HIGH STREET"]
    bcds1.patient.sex = 'M'
    bcds1.patient.nhs_number = '0000000000'
    bcds1.patient.date_of_birth = datetime.date(1958, 4, 14)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 1)

    bcds1.patient_charge_pence = 5630

    # Treatments: "Fillings x 1, Examination (9317), Ethnic Origin 16"
    bcds1.treatments = [
        treatments.TREATMENT_CATEGORY(2),
        treatments.PERMANENT_FILLINGS(1),
        treatments.EXAMINATION,
        treatments.ETHNIC_ORIGIN_ANY_OTHER_ETHNIC_GROUP,
    ]

    return bcds1


def from_model(bcds1, patient, episode):
    demographics = patient.demographics()
    demographics.surname = "ALVERCHURCH"
    demographics.first_name = "CARL"
    demographics.house_number_or_name = "31"
    demographics.street = "HIGH STREET"
    demographics.sex = "Male"
    demographics.date_of_birth = datetime.date(1958, 4, 14)
    demographics.ethnicity = "Other ethnic group"
    demographics.save()

    episode.fp17treatmentcategory_set.update(
        treatment_category="Band 2",
    )

    episode.fp17clinicaldataset_set.update(
        permanent_fillings=1,
        examination=True,
    )

    episode.fp17exemptions_set.update(
        patient_charge_collected=56.30
    )

    episode.fp17incompletetreatment_set.update(
        date_of_acceptance=datetime.date(2017, 4, 1),
        completion_or_last_visit=datetime.date(2017, 4, 1)
    )
    translate_to_bdcs1(bcds1, episode)
