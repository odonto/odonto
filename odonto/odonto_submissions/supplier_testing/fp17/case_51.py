import datetime
from odonto.odonto_submissions.serializers import translate_to_bdcs1
from odonto.models import Fp17ClinicalDataSet
from fp17 import treatments


def annotate(bcds1):
    bcds1.patient.surname = "BARLASTON"
    bcds1.patient.forename = "SALLY"
    bcds1.patient.address = ["1 HIGH STREET"]
    bcds1.patient.sex = 'F'
    bcds1.patient.nhs_number = '0000000000'
    bcds1.patient.date_of_birth = datetime.date(1958, 1, 23)

    bcds1.date_of_acceptance = datetime.date(2022, 4, 1)
    bcds1.date_of_completion = datetime.date(2022, 4, 1)

    bcds1.patient_charge_pence = 2060

    # Treatments: "Examination (9317), Recall Interval (9172 9), Scale &
    # Polish, Ethnic Origin 1"
    bcds1.treatments = [
        treatments.TREATMENT_CATEGORY(1),
        treatments.EXAMINATION,
        treatments.ETHNIC_ORIGIN_1_WHITE_BRITISH,
        treatments.CUSTOM_MADE_OCCLUSAL_APPLIANCE_HARD_BITE,
        treatments.DENTURE_ADDITIONS_RELINE_REBASE
    ]

    return bcds1


def from_model(bcds1, patient, episode):
    demographics = patient.demographics()
    demographics.surname = "Barlaston"
    demographics.first_name = "Sally"
    demographics.house_number_or_name = "1"
    demographics.street = "HIGH STREET"
    demographics.sex = "Female"
    demographics.date_of_birth = datetime.date(1958, 1, 23)
    demographics.ethnicity = "White british"
    demographics.save()
    episode.fp17treatmentcategory_set.update(
        treatment_category="Band 1",
    )

    episode.fp17clinicaldataset_set.update(
        examination=True,
        denture_additions_reline_rebase=True,
        custom_made_occlusal_appliance=Fp17ClinicalDataSet.HARD
    )

    episode.fp17exemptions_set.update(
        patient_charge_collected="20.60"
    )

    episode.fp17incompletetreatment_set.update(
        date_of_acceptance=datetime.date(2022, 4, 1),
        completion_or_last_visit=datetime.date(2022, 4, 1)
    )
    translate_to_bdcs1(bcds1, episode)
