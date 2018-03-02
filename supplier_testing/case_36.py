import datetime

from fp17 import treatments

from common import get_base, output


if __name__ == '__main__':
    bcds1 = get_base()

    bcds1.patient.surname = "ASLOCKTON"
    bcds1.patient.forename = "LAURA"
    bcds1.patient.address = ["32 HIGH STREET"]
    bcds1.patient.sex = 'F'
    bcds1.patient.date_of_birth = datetime.date(1968, 3, 24)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 1)

    bcds1.patient_charge_pence = 2060

    # Treatments: "Other Treatment (9399), Ethnic Origin 99"
    bcds1.treatments = [
        treatments.TREATMENT_CATEGORY_URGENT,

        treatments.ETHNIC_ORIGIN_PATIENT_DECLINED,
    ]

    output(bcds1)
