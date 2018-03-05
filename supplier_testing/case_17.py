import datetime

from fp17 import treatments

from common import get_base, output


if __name__ == '__main__':
    bcds1 = get_base()

    bcds1.patient.surname = "BUCKNELL"
    bcds1.patient.forename = "TOMMY"
    bcds1.patient.address = ["17 HIGH STREET"]
    bcds1.patient.sex = 'M'
    bcds1.patient.date_of_birth = datetime.date(2000, 3, 14)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 1)

    bcds1.patient_charge_pence = 14640

    # "Under 18"
    bcds1.excemption_remission = {'code': 0}  # FIXME

    # Treatments: "Upper Metal Denture 10, Lower Metal Denture 6, Decayed
    # Deciduous 0, Ethnic Origin 99"
    bcds1.treatments = [
        treatments.REGULATION_11_APPLIANCE,
        treatments.UPPER_DENTURE_METAL(10),
        treatments.LOWER_DENTURE_METAL(6),
        treatments.DECAYED_DECIDUOUS(0),
        treatments.ETHNIC_ORIGIN_PATIENT_DECLINED,
    ]

    output(bcds1)
