import datetime

from fp17 import treatments, exemptions

from common import get_base, output


if __name__ == '__main__':
    bcds1 = get_base()

    bcds1.patient.surname = "BYRON"
    bcds1.patient.forename = "HENRY"
    bcds1.patient.address = ["37 HIGH STREET"]
    bcds1.patient.sex = 'M'
    bcds1.patient.date_of_birth = datetime.date(1948, 3, 17)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 1)

    # "Pension Credits"
    bcds1.exemption_remission = {
        'code': exemptions.PENSION_CREDIT_GUARANTEE_CREDIT.EVIDENCE_SEEN,
    }

    # Treatments: "Filling 1"
    bcds1.treatments = [
        treatments.PERMANENT_FILLINGS_AND_SEALANT_RESTORATIONS(1),

        # 'Band 4'
        treatments.TREATMENT_CATEGORY_URGENT,
    ]

    output(bcds1)
