import datetime

from fp17 import treatments

from common import get_base, output


if __name__ == '__main__':
    bcds1 = get_base()

    bcds1.patient.surname = "BULWELL"
    bcds1.patient.forename = "LILY"
    bcds1.patient.address = ["18 HIGH STREET"]
    bcds1.patient.sex = 'F'
    bcds1.patient.date_of_birth = datetime.date(1968, 4, 28)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 1)

    # Treatments: "Ethnic Origin 1"
    bcds1.treatments = [
        treatments.PRESCRIPTION,

        treatments.ETHNIC_ORIGIN_1_WHITE_BRITISH,
    ]

    output(bcds1)
