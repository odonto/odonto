import datetime

from fp17 import treatments, exemptions

from common import get_base, output


if __name__ == '__main__':
    bcds1 = get_base()

    bcds1.patient.surname = "BORDESLEY"
    bcds1.patient.forename = "ANGELA"
    bcds1.patient.address = ["12 HIGH STREET"]
    bcds1.patient.sex = 'F'
    bcds1.patient.date_of_birth = datetime.date(1998, 11, 30)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 10)

    # "18 in full time education"
    bcds1.excemption_remission = {
        'code': excemptions.AGED_18_IN_FULL_TIME_EDUCATION.EVIDENCE_SEEN,
    }

    # Treatments: "Examination (9317), Scale and Polish, Radiographs x 1,
    # Fillings x 3, Recall Interval 24, Decayed Deciduous 4, Ethnic Origin 12"
    bcds1.treatments = [
        treatments.TREATMENT_CATEGORY(2),
        treatments.EXAMINATION,
        treatments.SCALE_AND_POLISH,
        treatments.RADIOGRAPHS(1),
        treatments.PERMANENT_FILLINGS_AND_SEALANT_RESTORATIONS(3),
        treatments.RECALL_INTERVAL(24),
        treatments.DECAYED_DECIDUOUS(4),
        treatments.ETHNIC_ORIGIN_12_BLACK_OR_BLACK_BRITISH_CARIBBEAN,
    ]

    output(bcds1)
