import datetime

from fp17 import treatments

from common import get_base, output


if __name__ == '__main__':
    bcds1 = get_base()

    bcds1.patient.surname = "CANNOCK"
    bcds1.patient.forename = "CAROL"
    bcds1.patient.address = ["23 HIGH STREET"]
    bcds1.patient.sex = 'F'
    bcds1.patient.date_of_birth = datetime.date(1950, 7, 29)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 1)

    # Treatments: "Examination (9317), Scale & Polish, Radiographs x 1,
    # Fillings x 1, Referral for Advanced Mandatory Services,  Ethnic Origin 6"
    bcds1.treatments = [
        treatments.TREATMENT_CATEGORY_BAND_2,

        treatments.ETHNIC_ORIGIN_6_WHITE_AND_ASIAN,
    ]

    output(bcds1)
