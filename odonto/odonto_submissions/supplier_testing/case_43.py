import datetime

from fp17 import treatments, exemptions


def annotate(bcds1):
    bcds1.patient.surname = "CARTWRIGHT"
    bcds1.patient.forename = "TOM"
    bcds1.patient.address = ["40 HIGH STREET"]
    bcds1.patient.sex = 'M'
    bcds1.patient.date_of_birth = datetime.date(1978, 12, 31)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 1)

    # "Universal Credit"
    bcds1.exemption_remission = {
        'code': exemptions.UNIVERSAL_CREDIT.EVIDENCE_SEEN,
    }

    # Treatments: "Examination, Extraction 1"
    bcds1.treatments = [
        treatments.EXAMINATION,
        treatments.EXTRACTION(1),

        # 'Band 4'
        treatments.TREATMENT_CATEGORY_URGENT,
    ]

    return bcds1
