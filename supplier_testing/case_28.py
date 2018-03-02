import datetime

from fp17 import treatments

from common import get_base, output


if __name__ == '__main__':
    bcds1 = get_base()

    bcds1.patient.surname = "HAMSTEAD"
    bcds1.patient.forename = "MONICA"
    bcds1.patient.address = ["28 HIGH STREET"]
    bcds1.patient.sex = 'F'
    bcds1.patient.date_of_birth = datetime.date(1989, 7, 27)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 1)

    bcds1.patient_charge_pence = 5630

    # Treatments: "Fillings x 1, Recall Interval (9172 12), Ethnic Origin 11"
    bcds1.treatments = [
        treatments.TREATMENT_CATEGORY_BAND_2,

        treatments.ETHNIC_ORIGIN_11_OTHER_ASIAN_BACKGROUND,
    ]

    output(bcds1)
