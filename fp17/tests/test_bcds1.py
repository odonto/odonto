from lxml import etree
from opal.core.test import OpalTestCase
from fp17 import treatments
from fp17 import bcds1
from fp17 import message


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
