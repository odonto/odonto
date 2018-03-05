import datetime

from fp17 import treatments

from common import get_base, output


if __name__ == '__main__':
    bcds1 = get_base()

    bcds1.patient.surname = "BOURNEVILLE"
    bcds1.patient.forename = "RITA"
    bcds1.patient.address = ["14 HIGH STREET"]
    bcds1.patient.sex = 'F'
    bcds1.patient.date_of_birth = datetime.date(1940, 6, 5)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 12)

    bcds1.patient_charge_pence = 5630

    # Treatments: "Fluoride Varnish, Filling x 1, Ethnic Origin 14"
    bcds1.treatments = [
        treatments.TREATMENT_CATEGORY_BAND_2,
        treatments.PERMANENT_FILLINGS_AND_SEALANT_RESTORATIONS(1),
        treatments.ETHNIC_ORIGIN_14_OTHER_BLACK_BACKGROUND,
    ]

    output(bcds1)
