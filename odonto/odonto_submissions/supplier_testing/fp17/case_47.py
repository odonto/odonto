import datetime
from odonto.odonto_submissions.serializers import translate_to_bdcs1
from fp17 import treatments


def annotate(bcds1):
    bcds1.patient.surname = "HATTON"
    bcds1.patient.forename = "TONY"
    bcds1.patient.address = ["34 HIGH STREET"]
    bcds1.patient.sex = 'M'
    bcds1.patient.nhs_number = '0000000000'
    bcds1.patient.date_of_birth = datetime.date(1970, 1, 31)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 5, 1)

    bcds1.patient_charge_pence = 24430

    # Treatments: "Scale and Polish,Examination (9317), Fluoride Varnish, Other Treatment (9399), Ethnic Origin 99 "
    bcds1.treatments = [
        treatments.TREATMENT_CATEGORY(3),
        treatments.INCOMPLETE_TREATMENT(2),
        treatments.ETHNIC_ORIGIN_PATIENT_DECLINED,
    ]

    return bcds1


def from_model(bcds1, patient, episode):
    demographics = patient.demographics()
    demographics.surname = "HATTON"
    demographics.first_name = "TONY"
    demographics.house_number_or_name = "34"
    demographics.street = "HIGH STREET"
    demographics.sex = "Male"
    demographics.ethnicity = "Patient declined"
    demographics.date_of_birth = datetime.date(1970, 1, 31)
    demographics.save()

    episode.fp17exemptions_set.update(
        patient_charge_collected=244.30
    )

    episode.fp17treatmentcategory_set.update(
        treatment_category="Band 3",
    )

    episode.fp17incompletetreatment_set.update(
        incomplete_treatment="Band 2",
        date_of_acceptance=datetime.date(2017, 4, 1),
        completion_or_last_visit=datetime.date(2017, 5, 1)
    )

    translate_to_bdcs1(bcds1, episode)
