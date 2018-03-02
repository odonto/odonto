import datetime

from fp17 import treatments

from common import get_base, output


if __name__ == '__main__':
    bcds1 = get_base()

    bcds1.patient.surname = "HADFIELD"
    bcds1.patient.forename = "DAVID"
    bcds1.patient.address = ["26 HIGH STREET"]
    bcds1.patient.sex = 'M'
    bcds1.patient.date_of_birth = datetime.date(1967, 5, 14)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 1)

    bcds1.patient_charge_pence = 5630

    # Treatments: "Examination (9317), Radiographs x 4,  Bridges x 2,
    # Antibiotic Items (9318 1), Recall Interval (9172 6), Ethnic Origin 9"
    bcds1.treatments = [
        treatments.TREATMENT_CATEGORY_BAND_3,

        treatments.ETHNIC_ORIGIN_9_ASIAN_OR_ASIAN_BRITISH_PAKISTANI,
    ]

    output(bcds1)
