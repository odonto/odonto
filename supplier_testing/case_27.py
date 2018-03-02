import datetime

from fp17 import treatments

from common import get_base, output


if __name__ == '__main__':
    bcds1 = get_base()

    bcds1.patient.surname = "HALL"
    bcds1.patient.forename = "AIDAN"
    bcds1.patient.address = ["27 HIGH STREET"]
    bcds1.patient.sex = 'M'
    bcds1.patient.date_of_birth = datetime.date(1980, 5, 31)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 20)

    # "Income Support"
    bcds1.excemption_remission = {'code': 0}  # FIXME

    # Treatments: "Fillings x 1, Other Treatment (9399), Decayed Permanent 11,
    # Ethnic Origin 10"
    bcds1.treatments = [
        treatments.TREATMENT_CATEGORY_BAND_2,

        treatments.ETHNIC_ORIGIN_11_OTHER_ASIAN_BACKGROUND,

        # FIXME: "Treatment on referral" service
    ]

    output(bcds1)
