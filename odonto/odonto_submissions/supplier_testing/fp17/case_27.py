import datetime
from odonto.odonto_submissions.serializers import translate_to_bdcs1
from fp17 import treatments, exemptions


def annotate(bcds1):
    bcds1.patient.surname = "HALL"
    bcds1.patient.forename = "AIDAN"
    bcds1.patient.address = ["27 HIGH STREET"]
    bcds1.patient.sex = 'M'
    bcds1.patient.nhs_number = '0000000000'
    bcds1.patient.date_of_birth = datetime.date(1980, 5, 31)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 20)

    # "Income Support"
    bcds1.exemption_remission = {
        'code': exemptions.INCOME_SUPPORT.EVIDENCE_SEEN,
    }

    # Treatments: "Fillings x 1, Other Treatment (9399), Decayed Permanent 11,
    # Ethnic Origin 10"
    bcds1.treatments = [
        treatments.TREATMENT_CATEGORY(2),

        treatments.ETHNIC_ORIGIN_11_OTHER_ASIAN_BACKGROUND,

        # "Treatment on referral" service
        treatments.REFERRAL_FOR_ADVANCED_MANDATORY_SERVICES(2),
    ]

    return bcds1


def from_model(bcds1, patient, episode):
    demographics = patient.demographics()
    demographics.surname = "HALL"
    demographics.first_name = "AIDAN"
    demographics.house_number_or_name = "27"
    demographics.street = "HIGH STREET"
    demographics.sex = "Male"
    demographics.date_of_birth = datetime.date(1980, 5, 31)
    demographics.ethnicity = "Other asian background"
    demographics.save()

    episode.fp17exemptions_set.update(
        income_support=True,
        evidence_of_exception_or_remission_seen=True
    )
    episode.fp17treatmentcategory_set.update(
        treatment_category="Band 2",
    )

    episode.fp17clinicaldataset_set.update(
        referral_for_advanced_mandatory_services_band=2
    )

    episode.fp17incompletetreatment_set.update(
        date_of_acceptance=datetime.date(2017, 4, 1),
        completion_or_last_visit=datetime.date(2017, 4, 20)
    )
    translate_to_bdcs1(bcds1, episode)
