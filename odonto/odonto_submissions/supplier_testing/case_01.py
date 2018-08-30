import datetime

from fp17 import treatments


def annotate(bcds1):
    bcds1.patient.surname = "BARLASTON"
    bcds1.patient.forename = "SALLY"
    bcds1.patient.address = ["1 HIGH STREET"]
    bcds1.patient.sex = 'F'
    bcds1.patient.date_of_birth = datetime.date(1958, 1, 23)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 1)

    bcds1.patient_charge_pence = 2060

    # Treatments: "Examination (9317), Recall Interval (9172 9), Scale &
    # Polish, Ethnic Origin 1"
    bcds1.treatments = [
        treatments.TREATMENT_CATEGORY(1),
        treatments.EXAMINATION,
        treatments.RECALL_INTERVAL(num_months=9),
        treatments.SCALE_AND_POLISH,
        treatments.ETHNIC_ORIGIN_1_WHITE_BRITISH,
    ]

    return bcds1
