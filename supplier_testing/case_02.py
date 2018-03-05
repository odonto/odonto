import datetime

from fp17 import treatments

from common import get_base, output


if __name__ == '__main__':
    bcds1 = get_base()

    bcds1.patient.surname = "BARNT"
    bcds1.patient.forename = "ANNIE"
    bcds1.patient.address = ["2 HIGH STREET"]
    bcds1.patient.sex = 'F'
    bcds1.patient.date_of_birth = datetime.date(1985, 7, 5)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 1)

    bcds1.patient_charge_pence = 5630

    # Treatments: "Filling x 1, Recall Interval 6, Ethnic Origin 2"
    bcds1.treatments = [
        treatments.TREATMENT_CATEGORY(2),
        treatments.RECALL_INTERVAL(num_months=6),
        treatments.ETHNIC_ORIGIN_2_WHITE_IRISH,
    ]

    output(bcds1)
