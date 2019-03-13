import datetime

from fp17 import treatments


def annotate(bcds1):
    bcds1.patient.surname = "BERKSWELL"
    bcds1.patient.forename = "KEITH"
    bcds1.patient.address = ["8 HIGH STREET"]
    bcds1.patient.sex = 'M'
    bcds1.patient.date_of_birth = datetime.date(1947, 5, 5)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 1)

    # Treatments: "Ethnic Origin 8, Missing Permanent 0"
    bcds1.treatments = [
        treatments.BRIDGE_REPAIRS,
        treatments.MISSING_PERMANENT(0),
        treatments.ETHNIC_ORIGIN_8_ASIAN_OR_ASIAN_BRITISH_INDIAN,
    ]

    return bcds1
