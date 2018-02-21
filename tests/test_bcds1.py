import datetime

from fp17.bcds1 import BCDS1Message, SCHEDULE_QUERY_TRUE
from fp17.patient import Patient


def test_valid():
    msg = BCDS1Message()
    msg.message_reference_number = 123456
    msg.performer_number = 123456
    msg.dpb_pin = 123456
    msg.contract_number = 1234567890
    msg.location = 123456

    msg.patient = Patient()
    msg.patient.sex = 'M'
    msg.patient.date_of_birth = datetime.date(1985, 12, 16)
    msg.patient.title = "Mr"
    msg.patient.forename = "Chris"
    msg.patient.surname = "Lamb"
    msg.patient.nhs_number = 'A123456789'
    msg.patient.national_insurance_number = 'J12345679'
    msg.patient.address = ["Address line {}".format(x) for x in range(5)]
    msg.patient.postcode = 'NW1 1AA'

    msg.provider_declaration = 65
    msg.schedule_query = SCHEDULE_QUERY_TRUE

    msg.date_of_acceptance = datetime.date(2018, 1, 1)
    msg.date_of_completion = datetime.date(2018, 1, 2)
    msg.date_of_examination = datetime.date(2018, 1, 3)

    msg.types_of_claims = [{
        'initial_registration': False,
        'reregistration': False,
        'care_of_other_dentist': False,
        'occasional_treatment_only': False,
        'treatment_on_referral': False,
        'part_nhs_private': False,
    }]

    msg.treatment_arrangements = {
        'transfer_to_continuing_care': False,
        'treatment_necessitated_by_trauma': False,
        'orthodontic_radiographs_or_study_casts': False,
        'disability_fee': False,
    }

    msg.patient_charge_pence = 1
    msg.patient_charge_currency = 'GBP'

    v = msg.get_validator()

    assert not v.errors

    root = msg.generate_xml()
    BCDS1Message.validate_xml(root)

def test_validation():
    msg = BCDS1Message()

    errors = msg.get_errors()
    assert 'required field' in errors['message_reference_number']

    msg.message_reference_number = 12345
    errors = msg.get_errors()
    assert 'min value is 100000' in errors['message_reference_number']

    msg.message_reference_number = 1234567
    errors = msg.get_errors()
    assert 'max value is 999999' in errors['message_reference_number']

    msg.message_reference_number = 123456
    assert 'clrn' not in msg.get_errors()
