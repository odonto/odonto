import datetime

from fp17 import treatments, exemptions


def annotate(bcds1):
    bcds1.patient.surname = "HALL"
    bcds1.patient.forename = "AIDAN"
    bcds1.patient.address = ["27 HIGH STREET"]
    bcds1.patient.sex = 'M'
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
        treatments.REFERRAL_FOR_ADVANCED_MANDATORY_SERVICES_LEGACY,
    ]

    return bcds1
