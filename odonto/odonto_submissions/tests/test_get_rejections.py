from opal.core.test import OpalTestCase
from odonto.odonto_submissions.management.commands import get_rejections
from odonto.episode_categories import FP17Episode, FP17OEpisode
from odonto.odonto_submissions.models import Submission
from unittest.mock import mock_open, patch

MODULE_ROUTE = "odonto.odonto_submissions.management.commands.get_rejections"

class GetRejectionsTestCase(OpalTestCase):
    def setUp(self):
        self.cmd = get_rejections.Command()
        self.patient, self.episode = self.new_patient_and_episode_please()
        self.episode.stage = FP17Episode.SUBMITTED
        self.episode.category_name = FP17Episode.display_name
        self.episode.save()
        self.episode.submission_set.create(
            state=Submission.REJECTED_BY_COMPASS,
            rejection="faulty"
        )
        self.episode.fp17dentalcareprovider_set.update(
            provider_location_number="29 Acacia Road"
        )
        self.expected = {
            "category": FP17Episode.display_name,
            "location": "29 Acacia Road",
            "submit_link": f"http://ntghcomdent1/pathway/#/fp17-submit/{self.patient.id}/{self.episode.id}",
            "rejection_reason": "faulty"
        }

    def test_get_row(self):
        self.assertEqual(
            self.cmd.get_row(self.episode), self.expected
        )

    @patch(f"{MODULE_ROUTE}.csv")
    def test_handle_fp17(self, csv_mock):
        m = mock_open()
        MOCKING_FILE_NAME_OPEN = f"{MODULE_ROUTE}.open"

        with patch(MOCKING_FILE_NAME_OPEN, m, create=True):
            self.cmd.handle()

        csv_mock.DictWriter.return_value.writerow.assert_called_once_with(self.expected)

    @patch(f"{MODULE_ROUTE}.csv")
    def test_handle_fp17o(self, csv_mock):
        self.episode.category_name = FP17OEpisode.display_name
        self.episode.save()
        self.expected["category"] = FP17OEpisode.display_name
        l = f"http://ntghcomdent1/pathway/#/fp17-o-submit/{self.patient.id}/{self.episode.id}"
        self.expected["submit_link"] = l
        m = mock_open()
        MOCKING_FILE_NAME_OPEN = f"{MODULE_ROUTE}.open"

        with patch(MOCKING_FILE_NAME_OPEN, m, create=True):
            self.cmd.handle()

        csv_mock.DictWriter.return_value.writerow.assert_called_once_with(self.expected)
