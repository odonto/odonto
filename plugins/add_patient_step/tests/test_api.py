from django.urls import reverse
from opal.core.test import OpalTestCase
from plugins.add_patient_step.api import DemographicsSearch


class DemographicsSearchTestCase(OpalTestCase):
    def setUp(self):
        self.naked_url = reverse("demographics-search-list")
        self.client.login(
            username=self.user.username, password=self.PASSWORD
        )
        self.url = "{}?nhs_number=111".format(self.naked_url)

    def test_no_nhs_number(self):
        response = self.client.get(self.naked_url)
        self.assertEqual(
            response.status_code, 400
        )

    def test_patient_found_locally(self):
        patient, _ = self.new_patient_and_episode_please()
        patient.demographics_set.update(
            nhs_number="111",
            first_name="Jane"
        )
        expected = self.client.get(self.url)
        self.assertEqual(
            expected.status_code, 200
        )
        result = expected.data
        self.assertEqual(
            result["status"], DemographicsSearch.PATIENT_FOUND_IN_APPLICATION
        )
        self.assertEqual(result["patient"]["id"], patient.id)

    def test_patient_not_found(self):
        expected = self.client.get(self.url)
        self.assertEqual(expected.status_code, 200)
        self.assertEqual(
            expected.data["status"], DemographicsSearch.PATIENT_NOT_FOUND
        )
