import datetime

from fp17 import treatments

from common import get_base, output


if __name__ == '__main__':
    bcds1 = get_base()

    bcds1.patient.surname = "ALBRIGHTON"
    bcds1.patient.forename = "GARY"
    bcds1.patient.address = ["29 HIGH STREET"]
    bcds1.patient.sex = 'M'
    bcds1.patient.date_of_birth = datetime.date(1966, 10, 30)

    bcds1.date_of_acceptance = datetime.date(2017, 5, 1)
    bcds1.date_of_completion = datetime.date(2017, 5, 1)

    # Treatments: "Other Treatment (9399), Ethnic Origin 13"
    bcds1.treatments = [
        treatments.TREATMENT_CATEGORY(1),
        treatments.OTHER_TREATMENT,
        treatments.ETHNIC_ORIGIN_13_BLACK_OR_BLACK_BRITISH_AFRICAN,

        # "Further treatment within 2 months" service
        treatments.FURTHER_TREATMENT_WITHIN_TWO_MONTHS
    ]

    output(bcds1)
