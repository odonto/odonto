import datetime
from odonto import models
from odonto.odonto_submissions.serializers import translate_to_bdcs1
from fp17 import treatments, exemptions


def annotate(bcds1):
    bcds1.patient.surname = "BUCKNELL"
    bcds1.patient.forename = "TOMMY"
    bcds1.patient.address = ["17 HIGH STREET"]
    bcds1.patient.sex = 'M'
    bcds1.patient.nhs_number = '0000000000'
    bcds1.patient.date_of_birth = datetime.date(2000, 3, 14)

    bcds1.date_of_acceptance = datetime.date(2017, 4, 1)
    bcds1.date_of_completion = datetime.date(2017, 4, 1)

    bcds1.patient_charge_pence = 14640

    # "Under 18"
    bcds1.exemption_remission = {
        'code': exemptions.PATIENT_UNDER_18.EVIDENCE_SEEN,
    }

    # Treatments: "Upper Metal Denture 10, Lower Metal Denture 6, Decayed
    # Deciduous 0, Ethnic Origin 99"
    bcds1.treatments = [
        treatments.REGULATION_11_APPLIANCE,
        treatments.UPPER_DENTURE_METAL(10),
        treatments.LOWER_DENTURE_METAL(6),
        treatments.ETHNIC_ORIGIN_PATIENT_DECLINED,
    ]

    return bcds1


def from_model(bcds1, patient, episode):
    demographics = patient.demographics()
    demographics.surname = "BUCKNELL"
    demographics.first_name = "TOMMY"
    demographics.house_number_or_name = "17"
    demographics.street = "HIGH STREET"
    demographics.sex = "Male"
    demographics.date_of_birth = datetime.date(2000, 3, 14)
    demographics.ethnicity = "Patient declined"
    demographics.save()

    episode.fp17exemptions_set.update(
        patient_charge_collected=146.40
    )

    episode.fp17exemptions_set.update(
        patient_under_18=True,
        evidence_of_exception_or_remission_seen=True
    )

    episode.fp17treatmentcategory_set.update(
        treatment_category=models.Fp17TreatmentCategory.REGULATION_11_REPLACEMENT_APPLIANCE
    )

    episode.fp17clinicaldataset_set.update(
        upper_denture_metal=10,
        lower_denture_metal=6,
        decayed_teeth_deciduous=0
    )

    episode.fp17incompletetreatment_set.update(
        date_of_acceptance=datetime.date(2017, 4, 1),
        completion_or_last_visit=datetime.date(2017, 4, 1)
    )
    translate_to_bdcs1(bcds1, episode)
