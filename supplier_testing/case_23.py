import datetime

from fp17 import treatments


def annotate(bcds1):
    bcds1.patient.surname = "CANNOCK"
    bcds1.patient.forename = "CAROL"
    bcds1.patient.address = ["23 HIGH STREET"]
    bcds1.patient.sex = 'F'
    bcds1.patient.date_of_birth = datetime.date(1950, 7, 29)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 1)

    # Treatments: "Examination (9317), Scale & Polish, Radiographs x 1,
    # Fillings x 1, Referral for Advanced Mandatory Services,  Ethnic Origin 6"
    bcds1.treatments = [
        treatments.TREATMENT_CATEGORY(2),
        treatments.SCALE_AND_POLISH,
        treatments.RADIOGRAPHS(1),
        treatments.PERMANENT_FILLINGS_AND_SEALANT_RESTORATIONS(1),
        treatments.REFERRAL_FOR_ADVANCED_MANDATORY_SERVICES_LEGACY,
        treatments.ETHNIC_ORIGIN_6_WHITE_AND_ASIAN,
    ]

    return bcds1
