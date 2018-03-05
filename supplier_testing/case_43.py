import datetime

from fp17 import treatments

from common import get_base, output


if __name__ == '__main__':
    bcds1 = get_base()

    bcds1.patient.surname = "CARTWRIGHT"
    bcds1.patient.forename = "TOM"
    bcds1.patient.address = ["40 HIGH STREET"]
    bcds1.patient.sex = 'M'
    bcds1.patient.date_of_birth = datetime.date(1978, 12, 31)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 1)

    # "Universal Credit"
    bcds1.excemption_remission = {'code': 0}  # FIXME

    # Treatments: "Examination, Extraction 1"
    bcds1.treatments = [
        treatments.EXAMINATION,
        treatments.EXTRACTION(1),

        # FIXME: Spreadsheet refers to unknown 'Band 4'
    ]

    output(bcds1)
