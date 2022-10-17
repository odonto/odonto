import datetime
from lxml import etree
import re
from opal.core.test import OpalTestCase
from fp17 import treatments
from fp17 import bcds1
from fp17 import message


class BCDS1TestCase(OpalTestCase):
    def test_bcds1(self):
        our_bdcs1 = bcds1.BCDS1()
        our_bdcs1.message_reference_number = 123456
        our_bdcs1.performer_number = 234567
        our_bdcs1.contract_number = 1234567891012
        our_bdcs1.gdc_number = "1234567890"
        our_bdcs1.dpb_pin = "456789"
        our_bdcs1.location = 345678
        patient = bcds1.Patient()
        patient.sex = "F"
        patient.date_of_birth = datetime.date(2000, 1, 2)
        patient.forename = "Jane"
        patient.surname = "Austin"
        patient.address = "1 Northumbria Rd"
        our_bdcs1.patient = patient
        result = our_bdcs1.generate_xml()
        self.assertEqual(result.attrib['clrn'], '123456')
        self.assertEqual(result.attrib['perf'], '234567')
        self.assertEqual(result.attrib['pin'], '456789')
        self.assertEqual(result.attrib['gdcno'], '1234567890')
        self.assertEqual(result.attrib['cno'], '1234567891012')
        self.assertEqual(result.attrib['loc'], '345678')


class PatientTestCase(OpalTestCase):
    def test_email_regex(self):
        regex = re.compile(bcds1.Patient.Meta.schema["email"]["regex"])
        self.assertTrue(
            regex.match("Jane.doe@nhs.net")
        )
        self.assertFalse(
            regex.match("Jane.doe.nhs.net")
        )
        self.assertFalse(
            regex.match("Janedoe@nhsnet")
        )

    def test_phone_number_regex(self):
        regex = re.compile(bcds1.Patient.Meta.schema["phone_number"]["regex"])
        self.assertTrue(
            regex.match("01111111111")
        )
        self.assertFalse(
            regex.match("11111111111")
        )

        # too long
        self.assertFalse(
            regex.match("011111111111")
        )


class CreateTreatmentsTestCase(OpalTestCase):
    def setUp(self):
        self.bdcs1 = bcds1.BCDS1()
        self.root = etree.Element("bcds1")

    def test_treatment_with_no_extra_attrs(self):
        treatment = treatments.REGULATION_11_APPLIANCE
        self.bdcs1.create_treatments(self.root, "tst", message.flatten([treatment]))
        self.assertEqual(
            etree.tostring(self.root, encoding=str),
            '<bcds1><tst><reptrtty trtcd="9162"/></tst></bcds1>',
        )

    def test_treatment_with_instance_count(self):
        treatment = treatments.EXTRACTION(1)
        self.bdcs1.create_treatments(self.root, "tst", message.flatten([treatment]))
        self.assertEqual(
            etree.tostring(self.root, encoding=str),
            '<bcds1><tst><reptrtty trtcd="9307" noins="01"/></tst></bcds1>',
        )

    def test_treatment_with_teeth(self):
        treatment = treatments.ORTHODONTIC_EXTRACTIONS(["14"])
        self.bdcs1.create_treatments(self.root, "tst", message.flatten([treatment]))
        self.assertEqual(
            etree.tostring(self.root, encoding=str),
            '<bcds1><tst><reptrtty trtcd="9408"><toid>14</toid></reptrtty></tst></bcds1>',
        )


class TreatmentTestCase(OpalTestCase):
    def test_equality_with_instance_count(self):
        bridges_fitted_1 = treatments.BRIDGES_FITTED(10)
        bridges_fitted_2 = treatments.BRIDGES_FITTED(10)
        self.assertEqual(bridges_fitted_1, bridges_fitted_2)

    def test_equality_fail_with_instance_count(self):
        bridges_fitted_1 = treatments.BRIDGES_FITTED(9)
        bridges_fitted_2 = treatments.BRIDGES_FITTED(10)
        self.assertNotEqual(bridges_fitted_1, bridges_fitted_2)

    def test_equality_without_instance_count(self):
        self.assertEqual(
            treatments.REGULATION_11_APPLIANCE, treatments.REGULATION_11_APPLIANCE
        )

    def test_equality_fail_without_instance_count(self):
        self.assertNotEqual(
            treatments.REGULATION_11_APPLIANCE, treatments.TREATMENT_COMPLETED
        )

    def test_equality_fail_with_teeth(self):
        self.assertNotEqual(
            treatments.ORTHODONTIC_EXTRACTIONS(["14"]),
            treatments.ORTHODONTIC_EXTRACTIONS(["15"])
        )

    def test_equality_success_with_teeth(self):
        self.assertEqual(
            treatments.ORTHODONTIC_EXTRACTIONS(["14"]),
            treatments.ORTHODONTIC_EXTRACTIONS(["14"])
        )

    def test_equality_fail_with_multiple_teeth(self):
        self.assertNotEqual(
            treatments.ORTHODONTIC_EXTRACTIONS(["15", "16"]),
            treatments.ORTHODONTIC_EXTRACTIONS(["15", "17"])
        )

    def test_equality_success_with_multiple_teeth(self):
        self.assertEqual(
            treatments.ORTHODONTIC_EXTRACTIONS(["15", "16"]),
            treatments.ORTHODONTIC_EXTRACTIONS(["15", "16"])
        )
