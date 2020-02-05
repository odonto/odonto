import datetime
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
        self.episode.fp17dentalcareprovider_set.update(performer="Dorothy Dentist")
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
            "date": None,
            "location": "29 Acacia Road",
            "performer": "Dorothy Dentist",
            "submit_link": f"http://ntghcomdent1/pathway/#/fp17-submit/{self.patient.id}/{self.episode.id}",
            "rejection_reason": "faulty"
        }

    def test_get_row(self):
        self.assertEqual(
            self.cmd.get_row(self.episode, "faulty"), self.expected
        )

    @patch(f"{MODULE_ROUTE}.csv")
    def test_handle_fp17(self, csv_mock):
        m = mock_open()
        MOCKING_FILE_NAME_OPEN = f"{MODULE_ROUTE}.open"

        with patch(MOCKING_FILE_NAME_OPEN, m, create=True):
            self.cmd.handle()
        self.assertEqual(
            csv_mock.DictWriter.return_value.writerow.call_args_list[0][0][0],
            self.expected
        )

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

        self.assertEqual(
            csv_mock.DictWriter.return_value.writerow.call_args_list[0][0][0],
            self.expected
        )

    def test_get_rows_without_a_performer(self):
        self.episode.category_name = FP17OEpisode.display_name
        self.episode.stage = FP17Episode.OPEN
        self.episode.save()
        self.episode.fp17dentalcareprovider_set.update(
            performer=None
        )
        result = self.cmd.get_rows_without_a_performer()
        self.assertEqual(
            len(result), 1
        )
        self.assertEqual(
            result[0]["rejection_reason"],
            "No performer recorded"
        )

    def test_get_old_unsubmitted_fp17s_rows(self):
        self.episode.category_name = FP17Episode.display_name
        self.episode.stage = FP17Episode.OPEN
        self.episode.save()
        self.episode.fp17incompletetreatment_set.update(
            completion_or_last_visit=datetime.date(2019, 6, 7)
        )
        result = self.cmd.get_old_unsubmitted_fp17s_rows()
        self.assertEqual(
            len(result), 1
        )
        self.assertEqual(
            result[0]["rejection_reason"],
            "Episode completed on 07/06/2019 but not submitted"
        )

    def test_get_no_completion_date_rows(self):
        self.episode.category_name = FP17Episode.display_name
        self.episode.stage = FP17Episode.OPEN
        self.episode.save()
        self.episode.fp17incompletetreatment_set.update(
            date_of_acceptance=datetime.date(2019, 6, 7),
            completion_or_last_visit=None
        )
        result = self.cmd.get_no_completion_date_rows()
        self.assertEqual(
            len(result), 1
        )
        self.assertEqual(
            result[0]["rejection_reason"],
            "Episode has not completion date and is not submitted but episode was accepted on 07/06/2019"
        )
