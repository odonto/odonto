from opal.core.test import OpalTestCase

from fp17.utils import min_digits, max_digits, strbool


class UtilsTestCase(OpalTestCase):
    def test_min_digits(self):
        self.assertEqual(min_digits(0), 0)
        self.assertEqual(min_digits(1), 1)
        self.assertEqual(min_digits(6), 100000)

    def test_max_digits(self):
        self.assertEqual(max_digits(0), 0)
        self.assertEqual(max_digits(1), 9)
        self.assertEqual(max_digits(6), 999999)

    def test_strbool(self):
        self.assertEqual(strbool(True), '1')
        self.assertEqual(strbool(False), '0')

        self.assertEqual(strbool([]), '0')
        self.assertEqual(strbool([1]), '1')
