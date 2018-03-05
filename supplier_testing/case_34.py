import datetime

from fp17 import treatments

from common import get_base, output


if __name__ == '__main__':
    bcds1 = get_base()

    bcds1.patient.surname = "ALVERCHURCH"
    bcds1.patient.forename = "CARL"
    bcds1.patient.address = ["31 HIGH STREET"]
    bcds1.patient.sex = 'M'
    bcds1.patient.date_of_birth = datetime.date(1958, 4, 14)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 1)

    bcds1.patient_charge_pence = 5630

    # Treatments: "Fillings x 1, Examination (9317), Ethnic Origin 16"
    bcds1.treatments = [
        treatments.TREATMENT_CATEGORY(2),
        treatments.PERMANENT_FILLINGS_AND_SEALANT_RESTORATIONS(1),
        treatments.EXAMINATION,
        treatments.ETHNIC_ORIGIN_ANY_OTHER_ETHNIC_GROUP,
    ]

    output(bcds1)
