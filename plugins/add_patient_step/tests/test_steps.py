from opal.core.test import OpalTestCase
from plugins.add_patient_step.steps import FindPatientStep


class FindPatientTestCase(OpalTestCase):
    def setUp(self):
        self.step = FindPatientStep()

    def test_to_dict(self):
        to_dicted = self.step.to_dict()
        self.assertEqual(
            to_dicted["search_end_point"],
            "/api/v0.1/demographics-search/"
        )
        self.assertEqual(
            to_dicted["display_name"],
            "Find patient"
        )