from opal.core.test import OpalTestCase
from fp17 import treatments


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
