import datetime

from fp17 import treatments, exemptions

from common import get_base, output


if __name__ == '__main__':
    bcds1 = get_base()

    bcds1.patient.surname = "BUTTON"
    bcds1.patient.forename = "ROY"
    bcds1.patient.address = ["35 HIGH STREET"]
    bcds1.patient.sex = 'M'
    bcds1.patient.date_of_birth = datetime.date(1964, 10, 17)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 1)

    # "Tax Credits (No Evidence Seen)"
    bcds1.exemption_remission = {
        'code': exemptions.PENSION_CREDIT_GUARANTEE_CREDIT.NO_EVIDENCE_SEEN,
    }

    # Treatments: "None"
    bcds1.treatments = [
        # 'Band 4'
        treatments.TREATMENT_CATEGORY_URGENT,
    ]

    output(bcds1)
