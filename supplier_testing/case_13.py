import datetime

from fp17 import treatments

from common import get_base, output


if __name__ == '__main__':
    bcds1 = get_base()

    bcds1.patient.surname = "BOTTESFORD"
    bcds1.patient.forename = "JULIAN"
    bcds1.patient.address = ["13 HIGH STREET"]
    bcds1.patient.sex = 'M'
    bcds1.patient.date_of_birth = datetime.date(1950, 2, 14)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 1)

    bcds1.patient_charge_pence = 2060

    # Treatments: "Examination (9317), Ethnic Origin 13"
    bcds1.treatments = [
        treatments.TREATMENT_CATEGORY_BAND_1,
        treatments.EXAMINATION,
        treatments.ETHNIC_ORIGIN_13_BLACK_OR_BLACK_BRITISH_AFRICAN,
    ]

    output(bcds1)
