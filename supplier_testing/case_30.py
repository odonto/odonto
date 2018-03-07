import datetime

from fp17 import treatments


def annotate(bcds1):
    bcds1.patient.surname = "ALBRIGHTON"
    bcds1.patient.forename = "GARY"
    bcds1.patient.address = ["29 HIGH STREET"]
    bcds1.patient.sex = 'M'
    bcds1.patient.date_of_birth = datetime.date(1966, 10, 30)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 1)

    bcds1.patient_charge_pence = 5630

    # Treatments: "Examination (9317), Extractions x 1, Recall Interval (9172
    # 9), Ethnic Origin 13 "
    bcds1.treatments = [
        treatments.TREATMENT_CATEGORY(2),
        treatments.EXTRACTION(1),
        treatments.RECALL_INTERVAL(9),
        treatments.ETHNIC_ORIGIN_13_BLACK_OR_BLACK_BRITISH_AFRICAN,
    ]

    return bcds1
