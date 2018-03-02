import datetime

from fp17 import treatments

from common import get_base, output


if __name__ == '__main__':
    bcds1 = get_base()

    bcds1.patient.surname = "BUTLERS"
    bcds1.patient.forename = "STACEY"
    bcds1.patient.address = ["20 HIGH STREET"]
    bcds1.patient.sex = 'F'
    bcds1.patient.date_of_birth = datetime.date(1980, 6, 14)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 1)

    # Treatments: "Ethnic Origin 3"
    bcds1.treatments = [
        treatments.BRIDGE_REPAIRS,

        treatments.ETHNIC_ORIGIN_3_WHITE_OTHER,
    ]

    output(bcds1)
