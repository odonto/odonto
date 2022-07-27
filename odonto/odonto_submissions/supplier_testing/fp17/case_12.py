import datetime
from odonto.odonto_submissions.serializers import translate_to_bdcs1
from fp17 import treatments, exemptions


def annotate(bcds1):
    bcds1.patient.surname = "BORDESLEY"
    bcds1.patient.forename = "ANGELA"
    bcds1.patient.address = ["12 HIGH STREET"]
    bcds1.patient.sex = 'F'
    bcds1.patient.nhs_number = '0000000000'
    bcds1.patient.date_of_birth = datetime.date(1998, 11, 30)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 10)

    # "18 in full time education"
    bcds1.exemption_remission = {
        'code': exemptions.AGED_18_IN_FULL_TIME_EDUCATION.EVIDENCE_SEEN,
    }

    # Treatments: "Examination (9317), Scale and Polish, Radiographs x 1,
    # Fillings x 3, Recall Interval 24, Decayed Deciduous 4, Ethnic Origin 12"
    bcds1.treatments = [
        treatments.TREATMENT_CATEGORY(2),
        treatments.EXAMINATION,
        treatments.SCALE_AND_POLISH,
        treatments.RADIOGRAPHS(1),
        treatments.PERMANENT_FILLINGS(3),
        treatments.RECALL_INTERVAL(24),
        treatments.DECAYED_DECIDUOUS(4),
        treatments.ETHNIC_ORIGIN_12_BLACK_OR_BLACK_BRITISH_CARIBBEAN,
    ]

    return bcds1


def from_model(bcds1, patient, episode):
    demographics = patient.demographics()
    demographics.surname = "BORDESLEY"
    demographics.first_name = "ANGELA"
    demographics.house_number_or_name = "12"
    demographics.street = "HIGH STREET"
    demographics.sex = "Female"
    demographics.date_of_birth = datetime.date(1998, 11, 30)
    demographics.ethnicity = "Black or black british caribbean"
    demographics.save()

    episode.fp17exemptions_set.update(
        aged_18_in_full_time_education=True,
        evidence_of_exception_or_remission_seen=True
    )

    episode.fp17recall_set.update(
        number_of_months=24
    )

    episode.fp17treatmentcategory_set.update(
        treatment_category="Band 2"
    )

    episode.fp17clinicaldataset_set.update(
        examination=True,
        scale_and_polish=True,
        radiographs_taken=1,
        permanent_fillings=3,
        decayed_teeth_deciduous=4
    )

    episode.fp17incompletetreatment_set.update(
        date_of_acceptance=datetime.date(2017, 4, 1),
        completion_or_last_visit=datetime.date(2017, 4, 10)
    )
    translate_to_bdcs1(bcds1, episode)
