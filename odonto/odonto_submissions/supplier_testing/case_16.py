import datetime

from fp17 import treatments


def annotate(bcds1):
    bcds1.patient.surname = "BROOME"
    bcds1.patient.forename = "RON"
    bcds1.patient.address = ["16 HIGH STREET"]
    bcds1.patient.sex = 'M'
    bcds1.patient.date_of_birth = datetime.date(1935, 4, 29)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 1)

    bcds1.patient_charge_pence = 2060

    # Treatments: "Filling x 1, Antibiotic items prescribed (9318 1), Ethnic
    # Origin 16"
    bcds1.treatments = [
        treatments.TREATMENT_CATEGORY_URGENT,
        treatments.ANTIBIOTIC_ITEMS(1),
        treatments.ETHNIC_ORIGIN_ANY_OTHER_ETHNIC_GROUP,
    ]

    return bcds1
