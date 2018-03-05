import datetime

from fp17 import treatments

from common import get_base, output


if __name__ == '__main__':
    bcds1 = get_base()

    bcds1.patient.surname = "CANLEY"
    bcds1.patient.forename = "VIOLET"
    bcds1.patient.address = ["22 HIGH STREET"]
    bcds1.patient.sex = 'F'
    bcds1.patient.date_of_birth = datetime.date(1929, 5, 25)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 1)

    # Treatments: "Filled Permanent 3, Ethnic Origin 5"
    bcds1.treatments = [
        treatments.REMOVAL_OF_SUTURES,
        treatments.FILLED_PERMANENT(3),
        treatments.ETHNIC_ORIGIN_5_WHITE_AND_BLACK_AFRICAN,
    ]

    output(bcds1)
