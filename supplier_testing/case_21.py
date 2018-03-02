import datetime

from fp17 import treatments

from common import get_base, output


if __name__ == '__main__':
    bcds1 = get_base()

    bcds1.patient.surname = "BUXTON"
    bcds1.patient.forename = "NIGEL"
    bcds1.patient.address = ["21 HIGH STREET "]
    bcds1.patient.sex = 'M'
    bcds1.patient.date_of_birth = datetime.date(1947, 1, 30)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 1)

    # Treatments: "Ethnic Origin 4"
    bcds1.treatments = [
        treatments.ARREST_OF_BLEEDING,
        treatments.ETHNIC_ORIGIN_4_WHITE_AND_BLACK_CARIBBEAN,
    ]

    output(bcds1)
