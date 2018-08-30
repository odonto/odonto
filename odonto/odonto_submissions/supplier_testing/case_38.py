import datetime

from fp17 import treatments, exemptions


def annotate(bcds1):
    bcds1.patient.surname = "BARNES"
    bcds1.patient.forename = "SUSAN"
    bcds1.patient.address = ["34 HIGH STREET"]
    bcds1.patient.sex = 'F'
    bcds1.patient.date_of_birth = datetime.date(1969, 7, 9)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 1)

    # "Expectant Mother"
    bcds1.exemption_remission = {
        'code': exemptions.EXPECTANT_MOTHER.EVIDENCE_SEEN,
    }

    # Treatments: "Examination"
    bcds1.treatments = [
        treatments.TREATMENT_CATEGORY(1),
        treatments.EXAMINATION,
    ]

    return bcds1
