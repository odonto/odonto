import datetime

from fp17 import treatments

from common import get_base, output


if __name__ == '__main__':
    bcds1 = get_base()

    bcds1.patient.surname = "BEDWORTH"
    bcds1.patient.forename = "TOBY"
    bcds1.patient.address = ["5 HIGH STREET"]
    bcds1.patient.sex = 'M'
    bcds1.patient.date_of_birth = datetime.date(1938, 4, 11)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 1)

    bcds1.patient_charge_pence = 7320

    # Treatments: "Upper Acrylic Denture 12, Ethnic Origin 5"
    bcds1.treatments = [
        treatments.REGULATION_11_APPLIANCE,

        treatments.ETHNIC_ORIGIN_5_WHITE_AND_BLACK_AFRICAN,
    ]

    output(bcds1)
