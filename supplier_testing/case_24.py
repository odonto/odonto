import datetime

from fp17 import treatments

from common import get_base, output


if __name__ == '__main__':
    bcds1 = get_base()

    bcds1.patient.surname = "CARLTON"
    bcds1.patient.forename = "LESLEY"
    bcds1.patient.address = ["24 HIGH STREET"]
    bcds1.patient.sex = 'F'
    bcds1.patient.date_of_birth = datetime.date(1967, 2, 7)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 1)

    # Treatments: "Ethnic Origin 7"
    bcds1.treatments = [
        # FIXME: "Domiciliary Services" service

        treatments.ETHNIC_ORIGIN_7_OTHER_MIXED_BACKGROUND,
    ]

    output(bcds1)
