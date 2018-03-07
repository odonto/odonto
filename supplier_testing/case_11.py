import datetime

from fp17 import treatments, exemptions


def annotate(bcds1):
    bcds1.patient.surname = "BINGHAM"
    bcds1.patient.forename = "AVRIL"
    bcds1.patient.address = ["11 HIGH STREET"]
    bcds1.patient.sex = 'F'
    bcds1.patient.date_of_birth = datetime.date(1969, 10, 7)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 5, 1)

    # "Nursing Mother (Evidence Not Seen)"
    bcds1.exemption_remission = {
        'code': exemptions.NURSING_MOTHER.NO_EVIDENCE_SEEN,
    }

    # Treatments: "Examination (9317), Radiographs x 2, Fillings x 2,
    # Extractions x 6, Referral for Advanced Mandatory Services,Recall Interval
    # (9172 12), Ethic Origin 11"
    bcds1.treatments = [
        treatments.TREATMENT_CATEGORY(3),
        treatments.RADIOGRAPHS(2),
        treatments.PERMANENT_FILLINGS_AND_SEALANT_RESTORATIONS(2),
        treatments.EXTRACTION(6),
        treatments.REFERRAL_FOR_ADVANCED_MANDATORY_SERVICES_LEGACY,
        treatments.RECALL_INTERVAL(num_months=12),
        treatments.ETHNIC_ORIGIN_11_OTHER_ASIAN_BACKGROUND,
    ]

    return bcds1
