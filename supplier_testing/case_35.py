import datetime

from fp17 import treatments

from common import get_base, output


if __name__ == '__main__':
    bcds1 = get_base()

    bcds1.patient.surname = "AMBERGATE"
    bcds1.patient.forename = "TINA"
    bcds1.patient.address = ["32 HIGH STREET"]
    bcds1.patient.sex = 'F'
    bcds1.patient.date_of_birth = datetime.date(1940, 11, 13)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 1)

    bcds1.patient_charge_pence = 2060

    # Treatments: "Scale & polish, Domicilliary Visit, Ethnic Origin 99"
    bcds1.treatments = [
        treatments.TREATMENT_CATEGORY(1),
        treatments.SCALE_AND_POLISH,
        treatments.DOMICILIARY_SERVICES,
        treatments.ETHNIC_ORIGIN_PATIENT_DECLINED,
    ]

    output(bcds1)
