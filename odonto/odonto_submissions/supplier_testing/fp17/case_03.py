import datetime

from fp17 import treatments, exemptions
from odonto.odonto_submissions.serializers import translate_to_bdcs1


def annotate(bcds1):
    bcds1.patient.surname = "BARROW"
    bcds1.patient.forename = "CHARLIE"
    bcds1.patient.address = ["3 HIGH STREET"]
    bcds1.patient.sex = 'M'
    bcds1.patient.nhs_number = '0000000000'
    bcds1.patient.date_of_birth = datetime.date(2001, 1, 24)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 5, 1)

    # "Under 18"
    bcds1.exemption_remission = {
        'code': exemptions.PATIENT_UNDER_18.EVIDENCE_SEEN,
    }

    # Treatments: "Radiographs x 2, Crown x 1, Filled Deciduous 2, Ethnic Origin 3"
    bcds1.treatments = [
        treatments.TREATMENT_CATEGORY(3),
        treatments.RADIOGRAPHS(2),
        treatments.CROWN(1),
        treatments.FILLED_TEETH_DECIDUOUS(2),
        treatments.ETHNIC_ORIGIN_3_WHITE_OTHER,
    ]

    return bcds1


def from_model(bcds1, patient, episode):
    demographics = patient.demographics()
    demographics.surname = "BARROW"
    demographics.first_name = "CHARLIE"
    demographics.house_number_or_name = "3"
    demographics.street = "HIGH STREET"
    demographics.sex = "Male"
    demographics.ethnicity = "White other"
    demographics.date_of_birth = datetime.date(2001, 1, 24)
    demographics.save()

    episode.fp17incompletetreatment_set.update(
        date_of_acceptance=datetime.date(2017, 4, 1),
        completion_or_last_visit=datetime.date(2017, 5, 1)
    )

    episode.fp17treatmentcategory_set.update(
        treatment_category="Band 3",
    )
    episode.fp17clinicaldataset_set.update(
        radiographs_taken=2,
        crowns_provided=1,
    )

    episode.fp17clinicaldataset_set.update(
        filled_teeth_deciduous=2,
    )

    episode.fp17exemptions_set.update(
        patient_under_18=True,
        evidence_of_exception_or_remission_seen=True
    )

    translate_to_bdcs1(bcds1, episode)
