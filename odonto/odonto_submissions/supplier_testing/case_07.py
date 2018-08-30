import datetime

from fp17 import treatments, exemptions


def annotate(bcds1):
    bcds1.patient.surname = "BELPER"
    bcds1.patient.forename = "MATTHEW"
    bcds1.patient.address = ["7 HIGH STREET"]
    bcds1.patient.sex = 'M'
    bcds1.patient.date_of_birth = datetime.date(2003, 3, 26)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 1)

    # "Under 18"
    bcds1.exemption_remission = {
        'code': exemptions.PATIENT_UNDER_18.EVIDENCE_SEEN,
    }

    # Treatments: "Missing Deciduous 10, Ethnic Origin 7"
    bcds1.treatments = [
        treatments.DENTURE_REPAIRS,
        treatments.MISSING_DECIDUOUS(10),
        treatments.ETHNIC_ORIGIN_7_OTHER_MIXED_BACKGROUND,
    ]

    return bcds1
