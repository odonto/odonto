import datetime

from fp17 import treatments

from common import get_base, output


if __name__ == '__main__':
    bcds1 = get_base()

    bcds1.patient.surname = "HAMSTEAD"
    bcds1.patient.forename = "MONICA"
    bcds1.patient.address = ["28 HIGH STREET"]
    bcds1.patient.sex = 'F'
    bcds1.patient.date_of_birth = datetime.date(1989, 7, 27)

    bcds1.date_of_acceptance = datetime.date(2017, 5, 1)
    bcds1.date_of_completion = datetime.date(2017, 5, 1)

    # Treatments: "Fillings x 1, Ethnic Origin 11"
    bcds1.treatments = [
        treatments.TREATMENT_CATEGORY(2),
        treatments.PERMANENT_FILLINGS_AND_SEALANT_RESTORATIONS(1),
        treatments.ETHNIC_ORIGIN_11_OTHER_ASIAN_BACKGROUND,

        # FIXME: "Free Repair Replacement" service
    ]

    output(bcds1)
