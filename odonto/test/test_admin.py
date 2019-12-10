from django.contrib.admin.sites import AdminSite
from odonto.admin import PatientAdmin
from opal.core.test import OpalTestCase
from opal.models import Patient


class PatientAdminTestCase(OpalTestCase):
    def setUp(self):
        self.patient, self.episode = self.new_patient_and_episode_please()
        self.site = AdminSite()
        self.admin = PatientAdmin(Patient, self.site)

    def test_patient_detail_link(self):
        self.assertEqual(
            self.admin.patient_detail_link(self.patient),
            "<a href='/patient/{0}/'>/patient/{0}/</a>".format(
                self.patient.id
            )
        )

    def test_view_on_site(self):
        self.assertEqual(
            self.admin.view_on_site(self.patient),
            '/patient/{}/'.format(self.patient.id)
        )
