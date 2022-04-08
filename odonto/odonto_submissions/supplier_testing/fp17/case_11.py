import datetime
from odonto.odonto_submissions.serializers import translate_to_bdcs1
from fp17 import treatments, exemptions


def annotate(bcds1):
    bcds1.patient.surname = "BINGHAM"
    bcds1.patient.forename = "AVRIL"
    bcds1.patient.address = ["11 HIGH STREET"]
    bcds1.patient.sex = 'F'
    bcds1.patient.nhs_number = '0000000000'
    bcds1.patient.date_of_birth = datetime.date(1969, 10, 7)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 5, 1)

    # "Nursing Mother (Evidence Not Seen)"
    bcds1.exemption_remission = {
        'code': exemptions.NURSING_MOTHER.NO_EVIDENCE_SEEN,
    }

    # Treatments: "Examination (9317), Radiographs x 2, Fillings x 2,
    # Extractions x 6, Referral for Advanced Mandatory Services,Recall Interval
    # (9172 12), Ethic Origin 11"
    bcds1.treatments = [
        treatments.TREATMENT_CATEGORY(3),
        treatments.RADIOGRAPHS(2),
        treatments.PERMANENT_FILLINGS(2),
        treatments.EXTRACTION(6),
        treatments.REFERRAL_FOR_ADVANCED_MANDATORY_SERVICES(3),
        treatments.RECALL_INTERVAL(num_months=12),
        treatments.ETHNIC_ORIGIN_11_OTHER_ASIAN_BACKGROUND,
    ]

    return bcds1


def from_model(bcds1, patient, episode):
    demographics = patient.demographics()
    demographics.surname = "BINGHAM"
    demographics.first_name = "AVRIL"
    demographics.house_number_or_name = "11"
    demographics.street = "HIGH STREET"
    demographics.sex = "Female"
    demographics.date_of_birth = datetime.date(1969, 10, 7)
    demographics.ethnicity = "Other asian background"
    demographics.save()

    episode.fp17treatmentcategory_set.update(
        treatment_category="Band 3"
    )

    episode.fp17exemptions_set.update(
        nursing_mother=True,
        evidence_of_exception_or_remission_seen=False
    )

    episode.fp17clinicaldataset_set.update(
        radiographs_taken=2,
        permanent_fillings=2,
        extractions=6,
        referral_for_advanced_mandatory_services_band=3,
    )

    episode.fp17recall_set.update(
        number_of_months=12
    )

    episode.fp17incompletetreatment_set.update(
        date_of_acceptance=datetime.date(2017, 4, 1),
        completion_or_last_visit=datetime.date(2017, 5, 1)
    )
    translate_to_bdcs1(bcds1, episode)
