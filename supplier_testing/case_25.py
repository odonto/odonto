import datetime

from fp17 import treatments


def annotate(bcds1):
    bcds1.patient.surname = "CHESTER"
    bcds1.patient.forename = "EDWARD"
    bcds1.patient.address = ["25 HIGH STREET"]
    bcds1.patient.sex = 'M'
    bcds1.patient.date_of_birth = datetime.date(1940, 12, 2)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 1)

    # Treatments: "Ethnic Origin 8"
    bcds1.treatments = [
        treatments.ETHNIC_ORIGIN_8_ASIAN_OR_ASIAN_BRITISH_INDIAN,
        treatments.SEDATION_SERVICES,
    ]

    return bcds1
