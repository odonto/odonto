"""
Defining Opal PatientLists
"""
from opal.models import Episode
from opal.core import patient_lists, menus

from odonto import models


class AllPatientsList(patient_lists.PatientList):
    display_name = 'All Patients'
    template_name = "lists/all_patients.html"

    schema = [
        models.Demographics,
        models.Fp17IncompleteTreatment
    ]

    def get_queryset(self, **kwargs):
        return Episode.objects.all()

    @classmethod
    def as_menuitem(cls):
        return menus.MenuItem(
            display=cls.get_display_name(),
            href="/#/list/{}".format(cls.get_slug()),
            active_pattern="/#/list/{}".format(cls.get_slug())
        )
