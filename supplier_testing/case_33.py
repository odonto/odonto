import datetime

from fp17 import treatments

from common import get_base, output


if __name__ == '__main__':
    bcds1 = get_base()

    bcds1.patient.surname = "ALSAGER"
    bcds1.patient.forename = "SAM"
    bcds1.patient.address = ["31 HIGH STREET"]
    bcds1.patient.sex = 'F'
    bcds1.patient.date_of_birth = datetime.date(1947, 8, 16)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 1)

    bcds1.patient_charge_pence = 5630

    # Treatments: "Fillings x 2, Scale and Polish, Radiographs x 2, Examination
    # (9317), Antibiotic Items Prescribed (9318 x 1), Other Treatment (9399),
    # Recall Interval (9172 18), Ethnic Origin 1, Best Practice Prevention"
    bcds1.treatments = [
        treatments.TREATMENT_CATEGORY(2),

        treatments.ETHNIC_ORIGIN_1_WHITE_BRITISH,
    ]

    output(bcds1)
