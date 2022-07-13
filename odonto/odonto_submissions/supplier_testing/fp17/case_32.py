import datetime
from odonto.odonto_submissions.serializers import translate_to_bdcs1
from fp17 import treatments


def annotate(bcds1):
    bcds1.patient.surname = "ALFRETON"
    bcds1.patient.forename = "RAY"
    bcds1.patient.address = ["30 HIGH STREET"]
    bcds1.patient.sex = 'M'
    bcds1.patient.nhs_number = '0000000000'
    bcds1.patient.date_of_birth = datetime.date(1978, 6, 28)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 1)

    # Treatments: "Fissure Sealants x 2, Ethnic Origin (9025 99)"
    bcds1.treatments = [
        treatments.TREATMENT_CATEGORY(2),
        treatments.FISSURE_SEALANTS(2),
        treatments.ETHNIC_ORIGIN_PATIENT_DECLINED,

        # "Treatment on referral" service
        treatments.REFERRAL_FOR_ADVANCED_MANDATORY_SERVICES(2),
    ]

    return bcds1


def from_model(bcds1, patient, episode):
    demographics = patient.demographics()
    demographics.surname = "ALFRETON"
    demographics.first_name = "RAY"
    demographics.house_number_or_name = "30"
    demographics.street = "HIGH STREET"
    demographics.sex = "Male"
    demographics.date_of_birth = datetime.date(1978, 6, 28)
    demographics.ethnicity = "Patient declined"
    demographics.save()

    episode.fp17treatmentcategory_set.update(
        treatment_category="Band 2",
    )

    episode.fp17clinicaldataset_set.update(
        referral_for_advanced_mandatory_services_band=2,
        fissure_sealants=2
    )

    episode.fp17incompletetreatment_set.update(
        date_of_acceptance=datetime.date(2017, 4, 1),
        completion_or_last_visit=datetime.date(2017, 4, 1)
    )
    translate_to_bdcs1(bcds1, episode)
