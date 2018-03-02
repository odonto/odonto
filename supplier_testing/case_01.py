import datetime

from fp17 import treatments

from common import get_base, output


if __name__ == '__main__':
    bcds1 = get_base()

    bcds1.patient.surname = "BARLASTON"
    bcds1.patient.forename = "SALLY"
    bcds1.patient.address = ["1 HIGH STREET"]
    bcds1.patient.sex = 'F'
    bcds1.patient.date_of_birth = datetime.date(1958, 1, 23)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 1)

    bcds1.patient_charge_pence = 2060

    # "Examination (9317), Recall Interval (9172 9), Scale & Polish, Ethnic Origin 1"
    bcds1.treatments = [
        treatments.TREATMENT_CATEGORY_BAND_1,
        treatments.EXAMINATION,
        treatments.RECALL_INTERVAL(months=9),
        treatments.SCALE_AND_POLISH,
        treatments.ETHNIC_ORIGIN_1_WHITE_BRITISH,
    ]

    output(bcds1)
