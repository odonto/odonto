import datetime
from odonto.odonto_submissions.serializers import translate_to_bdcs1
from fp17 import treatments


def annotate(bcds1):
    bcds1.patient.surname = "BROMSGROVE"
    bcds1.patient.forename = "GARY"
    bcds1.patient.address = ["15 HIGH STREET"]
    bcds1.patient.sex = 'M'
    bcds1.patient.nhs_number = '0000000000'
    bcds1.patient.date_of_birth = datetime.date(1970, 5, 27)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 5, 1)

    bcds1.patient_charge_pence = 24430

    # Treatments: "Extraction x 2, Upper Denture Acrylic 2 teeth, Recall
    # Interval 8, Ethnic Origin 15"
    bcds1.treatments = [
        treatments.TREATMENT_CATEGORY(3),
        treatments.EXTRACTION(2),
        treatments.UPPER_DENTURE_ACRYLIC(2),
        treatments.RECALL_INTERVAL(8),
        treatments.ETHNIC_ORIGIN_15_CHINESE,
        treatments.SEDATION_SERVICES,
    ]

    return bcds1


def from_model(bcds1, patient, episode):
    demographics = patient.demographics()
    demographics.surname = "BROMSGROVE"
    demographics.first_name = "GARY"
    demographics.house_number_or_name = "15"
    demographics.street = "HIGH STREET"
    demographics.sex = "Male"
    demographics.date_of_birth = datetime.date(1970, 5, 27)
    demographics.ethnicity = "Chinese"
    demographics.save()

    episode.fp17treatmentcategory_set.update(
        treatment_category="Band 3"
    )

    episode.fp17clinicaldataset_set.update(
        extractions=2,
        upper_denture_acrylic=2
    )

    episode.fp17recall_set.update(
        number_of_months=8
    )

    episode.fp17exemptions_set.update(
        patient_charge_collected="244.30"
    )

    episode.fp17otherdentalservices_set.update(
        sedation_services=True
    )

    episode.fp17incompletetreatment_set.update(
        date_of_acceptance=datetime.date(2017, 4, 1),
        completion_or_last_visit=datetime.date(2017, 5, 1)
    )
    translate_to_bdcs1(bcds1, episode)
