import datetime

from fp17 import treatments

from common import get_base, output


if __name__ == '__main__':
    bcds1 = get_base()

    bcds1.patient.surname = "HATTON"
    bcds1.patient.forename = "TONY"
    bcds1.patient.address = ["34 HIGH STREET"]
    bcds1.patient.sex = 'M'
    bcds1.patient.date_of_birth = datetime.date(1970, 1, 31)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 5, 1)

    bcds1.patient_charge_pence = 24430

    # Treatments: "Scale and Polish,Examination (9317), Fluoride Varnish, Other Treatment (9399), Ethnic Origin 99 "
    bcds1.treatments = [
        treatments.TREATMENT_CATEGORY(3),
    ]

    output(bcds1)
