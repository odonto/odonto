"""
Tests that if we have multiple exemptions we only use the one that
comes first
"""
import datetime
from django.contrib.auth.models import User
from odonto import models
from odonto.odonto_submissions.serializers import translate_to_bdcs1
from fp17 import treatments
from fp17 import exemptions


def annotate(bcds1):
    bcds1.patient.surname = "BARLASTON"
    bcds1.patient.forename = "SALLY"
    bcds1.patient.address = ["1 HIGH STREET"]
    bcds1.patient.sex = 'F'
    bcds1.patient.date_of_birth = datetime.date(1958, 1, 23)
    bcds1.patient.nhs_number = "7110493547"
    bcds1.date_of_acceptance = datetime.date(2022, 10, 2)
    bcds1.date_of_completion = datetime.date(2022, 10, 2)

    bcds1.treatments = [
        treatments.TREATMENT_CATEGORY(1),
        treatments.NON_MOLAR_ENDONTIC_TREATMENT(1),
        treatments.ETHNIC_ORIGIN_1_WHITE_BRITISH,
    ]
    bcds1.exemption_remission = {"code": exemptions.PATIENT_UNDER_18.NO_EVIDENCE_SEEN}

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
    demographics.hospital_number = "0123456789"
    demographics.nhs_number = "711 049 3547"
    demographics.save()
    episode.fp17treatmentcategory_set.update(
        treatment_category="Band 1",
    )
    episode.fp17incompletetreatment_set.update(
        date_of_acceptance=datetime.date(2022, 10, 2),
        completion_or_last_visit=datetime.date(2022, 10, 2)
    )
    episode.fp17clinicaldataset_set.update(
        non_molar_endodontic_treatment=1
    )
    # We should only see the patient under 18 exemptiom
    episode.fp17exemptions_set.update(
        patient_under_18=True,
        expectant_mother=True,
    )

    translate_to_bdcs1(bcds1, episode)
