import datetime

from fp17 import treatments


def annotate(bcds1):
    bcds1.patient.surname = "ALFRETON"
    bcds1.patient.forename = "RAY"
    bcds1.patient.address = ["30 HIGH STREET"]
    bcds1.patient.sex = 'M'
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
