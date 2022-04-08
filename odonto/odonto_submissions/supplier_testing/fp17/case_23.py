import datetime
from odonto.odonto_submissions.serializers import translate_to_bdcs1
from fp17 import treatments


def annotate(bcds1):
    bcds1.patient.surname = "CANNOCK"
    bcds1.patient.forename = "CAROL"
    bcds1.patient.address = ["23 HIGH STREET"]
    bcds1.patient.sex = 'F'
    bcds1.patient.nhs_number = '0000000000'
    bcds1.patient.date_of_birth = datetime.date(1950, 7, 29)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 1)

    # Treatments: "Examination (9317), Scale & Polish, Radiographs x 1,
    # Fillings x 1, Referral for Advanced Mandatory Services,  Ethnic Origin 6"
    bcds1.treatments = [
        treatments.TREATMENT_CATEGORY(2),
        treatments.SCALE_AND_POLISH,
        treatments.RADIOGRAPHS(1),
        treatments.PERMANENT_FILLINGS(1),
        treatments.REFERRAL_FOR_ADVANCED_MANDATORY_SERVICES(2),
        treatments.ETHNIC_ORIGIN_6_WHITE_AND_ASIAN,
    ]

    return bcds1


def from_model(bcds1, patient, episode):
    demographics = patient.demographics()
    demographics.surname = "CANNOCK"
    demographics.first_name = "CAROL"
    demographics.house_number_or_name = "23"
    demographics.street = "HIGH STREET"
    demographics.sex = "Female"
    demographics.date_of_birth = datetime.date(1950, 7, 29)
    demographics.ethnicity = "White and asian"
    demographics.save()

    episode.fp17treatmentcategory_set.update(
        treatment_category="Band 2"
    )

    episode.fp17clinicaldataset_set.update(
        scale_and_polish=True,
        radiographs_taken=1,
        permanent_fillings=1,
        referral_for_advanced_mandatory_services_band=2
    )

    episode.fp17incompletetreatment_set.update(
        date_of_acceptance=datetime.date(2017, 4, 1),
        completion_or_last_visit=datetime.date(2017, 4, 1)
    )
    translate_to_bdcs1(bcds1, episode)
