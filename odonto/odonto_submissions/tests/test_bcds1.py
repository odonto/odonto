import datetime

from opal.core.test import OpalTestCase

from fp17 import treatments
from fp17.bcds1 import BCDS1, Patient, Treatment, SCHEDULE_QUERY_TRUE


def gen_bcds1():
    msg = BCDS1()
    msg.message_reference_number = 12345
    msg.performer_number = 123456
    msg.dpb_pin = "123456"
    msg.contract_number = 1021700000
    msg.location = 123456

    msg.patient = Patient()
    msg.patient.sex = 'M'
    msg.patient.date_of_birth = datetime.date(1985, 12, 16)
    msg.patient.title = "MR"
    msg.patient.forename = "CHRIS"
    msg.patient.surname = "LAMB"
    msg.patient.nhs_number = 'A123456789'
    msg.patient.national_insurance_number = 'J12345679'
    msg.patient.address = ["ADDRESS LINE {}".format(x) for x in range(5)]
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

    msg.exemption_remission = {
        'code': 10,
        'supporting_details': "SUPPORTING DETAILS",
    }

    t1 = Treatment(code=1234, instance_count=1, teeth=['12'])
    t2 = Treatment(code=5678, instance_count=3, teeth=['12'])

    msg.treatments = [t1, t2]
    msg.treatments_specific = [t2, t1]

    msg.dental_chart = [{
        'tooth': '89',
        'annotation': 'BP',
    }]

    return msg


class BCDS1TestCase(OpalTestCase):
    def test_valid(self):
        msg = gen_bcds1()

        v = msg.get_validator()

        assert not v.errors

        root = msg.generate_xml()
        assert root.attrib['noseg'] == '8'

        msg.validate_xml(root)

    def test_validation(self):
        msg = gen_bcds1()
        delattr(msg, "message_reference_number")

        errors = msg.get_errors()
        assert 'required field' in errors['message_reference_number']

        msg.message_reference_number = 0
        errors = msg.get_errors()
        assert 'min value is 1' in errors['message_reference_number']

        msg.message_reference_number = 1234567
        errors = msg.get_errors()
        assert 'max value is 999999' in errors['message_reference_number']

        msg.message_reference_number = 123456
        assert 'clrn' not in msg.get_errors()

    def test_treatment_validation(self):
        msg = gen_bcds1()

        v = msg.get_validator()

        msg.treatments.append(
            treatments.REFERRAL_FOR_ADVANCED_MANDATORY_SERVICES_LEGACY()
        )

        errors = msg.get_errors()
        assert 'Legacy Advanced Mandatory Services used after 01/04/2014' in \
            errors['treatments']
