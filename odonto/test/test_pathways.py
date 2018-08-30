from opal.core.test import OpalTestCase
from odonto import pathways


class Fp17PathwaysTestCase(OpalTestCase):
    def test_link(self):
        result = pathways.Fp17Pathway.get_absolute_url(
            ngepisode=2, ngpatient=1
        )
        self.assertEqual(
            result, "/pathway/#/fp17/[[ 1 ]]/[[ 2 ]]/"
        )
