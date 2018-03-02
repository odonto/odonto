import datetime

from fp17 import treatments

from common import get_base, output


if __name__ == '__main__':
    bcds1 = get_base()

    bcds1.patient.surname = "BARROW"
    bcds1.patient.forename = "CHARLIE"
    bcds1.patient.address = ["3 HIGH STREET"]
    bcds1.patient.sex = 'M'
    bcds1.patient.date_of_birth = datetime.date(2001, 1, 24)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 5, 1)

    # "Under 18"
    bcds1.excemption_remission = {'code': 28}

    bcds1.treatments = [
        treatments.RADIOGRAPHS(2),
        treatments.CROWN(1),
        treatments.FILLED_TEETH_DECIDUOUS(2),
        treatments.ETHNIC_ORIGIN_WHITE_OTHER,
    ]

    output(bcds1)

