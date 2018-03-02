import datetime

from fp17 import treatments

from common import get_base, output


if __name__ == '__main__':
    bcds1 = get_base()

    bcds1.patient.surname = "BARNES"
    bcds1.patient.forename = "SUSAN"
    bcds1.patient.address = ["34 HIGH STREET"]
    bcds1.patient.sex = 'F'
    bcds1.patient.date_of_birth = datetime.date(1969, 7, 9)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 1)

    # "Expectant Mother"
    bcds1.excemption_remission = {'code': 0}  # FIXME

    # Treatments: "Examination"
    bcds1.treatments = [
        treatments.TREATMENT_CATEGORY_BAND_1,
    ]

    output(bcds1)
