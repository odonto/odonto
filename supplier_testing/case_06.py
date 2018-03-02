import datetime

from fp17 import treatments

from common import get_base, output


if __name__ == '__main__':
    bcds1 = get_base()

    bcds1.patient.surname = "BEESTON"
    bcds1.patient.forename = "TODD"
    bcds1.patient.address = ["6 HIGH STREET"]
    bcds1.patient.sex = 'M'
    bcds1.patient.date_of_birth = datetime.date(1956, 12, 3)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 1)

    # Treatments: "Antibiotic items (9318 1), Ethnic Origin 6"
    bcds1.treatments = [
        treatments.PRESCRIPTION,

        treatments.ETHNIC_ORIGIN_6_WHITE_AND_ASIAN,
    ]

    output(bcds1)
