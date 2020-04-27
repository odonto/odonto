from unittest import mock
from opal.core.test import OpalTestCase
from odonto import utils

@mock.patch('odonto.utils.datetime')
class CurrentTaxYearTestCase(OpalTestCase):
    def test_current_tax_year_pre_aprils(self, datetime):
        today = datetime.date(2020, 1, 1)
        tax_start = datetime.date(2019, 4, 1)
        datetime.date.today.return_value = today
        self.assertEqual(
            tax_start,
            today
        )

    def test_current_tax_year_post_april(self, datetime):
        today = datetime.date(2020, 5, 1)
        tax_start = datetime.date(2020, 4, 1)
        datetime.date.today.return_value = today
        self.assertEqual(
            tax_start,
            today
        )

    def test_current_tax_year_april(self, datetime):
        today = datetime.date(2020, 4, 3)
        tax_start = datetime.date(2020, 4, 1)
        datetime.date.today.return_value = today
        self.assertEqual(
            tax_start,
            today
        )