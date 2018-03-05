import datetime

from fp17 import treatments

from common import get_base, output


if __name__ == '__main__':
    bcds1 = get_base()

    bcds1.patient.surname = "BORAGE"
    bcds1.patient.forename = "ARNOLD"
    bcds1.patient.address = ["41 HIGH STREET"]
    bcds1.patient.sex = 'M'
    bcds1.patient.date_of_birth = datetime.date(1935, 11, 17)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 5, 1)

    bcds1.patient_charge_pence = 24430

    # Treatments: "Crowns x 2, Missing Permanent 8"
    bcds1.treatments = [
        treatments.TREATMENT_CATEGORY(3),
    ]

    output(bcds1)
