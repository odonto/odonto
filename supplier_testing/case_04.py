import datetime

from fp17 import treatments

from common import get_base, output


if __name__ == '__main__':
    bcds1 = get_base()

    bcds1.patient.surname = "BEARLEY"
    bcds1.patient.forename = "LANCE"
    bcds1.patient.address = ["4 HIGH STREET"]
    bcds1.patient.sex = 'M'
    bcds1.patient.date_of_birth = datetime.date(1959, 4, 5)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 1)

    bcds1.patient_charge_pence = 2060

    # Treatments: "Antibiotic Items (9318 1), Decayed Permanent 0, Missing
    # Permanent 1, Filled Permanent 12, Ethnic Origin 4"
    bcds1.treatments = [
        treatments.TREATMENT_CATEGORY_URGENT,
        treatments.ANTIBIOTIC_ITEMS(1),
        treatments.DECAYED_PERMANENT(0),
        treatments.MISSING_PERMANENT(1),
        treatments.FILLED_PERMANENT(12),
        treatments.ETHNIC_ORIGIN_4_WHITE_AND_BLACK_CARIBBEAN,
    ]

    output(bcds1)
