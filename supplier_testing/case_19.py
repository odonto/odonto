import datetime

from fp17 import treatments


def annotate(bcds1):
    bcds1.patient.surname = "BURTON"
    bcds1.patient.forename = "TANIA"
    bcds1.patient.address = ["19 HIGH STREET"]
    bcds1.patient.sex = 'F'
    bcds1.patient.date_of_birth = datetime.date(1950, 8, 16)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 1)

    # Treatments: "Ethnic Origin 2"
    bcds1.treatments = [
        treatments.DENTURE_REPAIRS,
        treatments.ETHNIC_ORIGIN_2_WHITE_IRISH,
    ]

    return bcds1
