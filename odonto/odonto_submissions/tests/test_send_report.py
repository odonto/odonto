import datetime
from opal.core.test import OpalTestCase
from unittest.mock import MagicMock, patch
from opal.models import Episode
from odonto.odonto_submissions.models import Submission, EpisodesBeingInvestigated
from odonto.episode_categories import FP17Episode
from odonto.odonto_submissions.management.commands import send_report

BASE_STR = "odonto.odonto_submissions.management.commands.send_report"


@patch(BASE_STR + ".send_mail")
@patch(BASE_STR + ".render_to_string")
@patch(BASE_STR + ".logger")
class GetResponsesTestCase(OpalTestCase):
    def setUp(self):
        self.cmd = send_report.Command()
        self.response = MagicMock()

    def get_episode(self):
        _, episode = self.new_patient_and_episode_please()
        episode.category_name = FP17Episode.display_name
        episode.stage = FP17Episode.SUBMITTED
        episode.save()
        episode.fp17incompletetreatment_set.update(
            completion_or_last_visit=datetime.date.today()
        )
        return episode

    def get_submission(self, episode, state):
        mock_str = "odonto.odonto_submissions.models.serializers.\
translate_episode_to_xml"
        with patch(mock_str) as m:
            m.return_value = ""
            submission = Submission.create(episode)
        submission.state = state
        submission.save()
        return submission

    def test_without_none(self, logger, render_to_string, send_mail):
        self.response.get_successfull_submissions.return_value = Submission.objects.all()
        self.response.get_rejected_submissions.return_value = {}
        self.cmd.send_email(self.response)
        ctx = render_to_string.call_args[0][1]
        expected_summary = {
            "FP17 Success": 0,
            "FP17 Rejected": 0,
            "FP17O Success": 0,
            "FP17O Rejected": 0,
        }
        self.assertEqual(ctx["summary"]["Latest response"], expected_summary)
        self.assertTrue(ctx["title"].startswith("Odonto response information for"))

    def test_with_success(self, logger, render_to_string, send_mail):
        episode = self.get_episode()
        self.get_submission(episode, Submission.SUCCESS)
        self.response.get_successfull_submissions.return_value = Submission.objects.all()
        self.response.get_rejected_submissions.return_value = {}
        self.cmd.send_email(self.response)
        ctx = render_to_string.call_args[0][1]
        expected_summary = {
            "FP17 Success": 1,
            "FP17 Rejected": 0,
            "FP17O Success": 0,
            "FP17O Rejected": 0,
        }
        self.assertEqual(ctx["summary"]["Latest response"], expected_summary)

        expected_fp17 = {
            'Oldest unsent': None,
            'Open': 0,
            'Success': 1
        }
        self.assertEqual(
            ctx["summary"]["FP17 current tax year"],
            expected_fp17
        )

        expected_fp17o = {
            'Open': 0,
            'Oldest unsent': None
        }
        self.assertEqual(
            ctx["summary"]["FP17O current tax year"],
            expected_fp17o
        )

        self.assertEqual(
            ctx["summary"]["FP17 all time"],
            expected_fp17
        )

        self.assertEqual(
            ctx["summary"]["FP17O all time"],
            expected_fp17o
        )

        self.assertTrue(ctx["title"].startswith("Odonto response information for"))
        self.assertFalse(ctx["title"].endswith("NEEDS INVESTIGATION"))

    def test_with_rejection(self, logger, render_to_string, send_mail):
        episode = self.get_episode()
        self.get_submission(episode, Submission.REJECTED_BY_COMPASS)
        self.response.get_successfull_submissions.return_value = Submission.objects.none()
        self.response.get_rejected_submissions.return_value = {
            Submission.objects.get(): "fail"
        }
        self.cmd.send_email(self.response)
        ctx = render_to_string.call_args[0][1]
        expected_summary = {
            "FP17 Success": 0,
            "FP17 Rejected": 1,
            "FP17O Success": 0,
            "FP17O Rejected": 0,
        }
        self.assertEqual(ctx["summary"]["Latest response"], expected_summary)

        expected_current_fp17 = {
            'Oldest unsent': datetime.date.today(),
            'Open': 0,
            'Rejected by compass': send_report.WarningField(1)
        }
        self.assertEqual(
            ctx["summary"]["FP17 current tax year"],
            expected_current_fp17
        )

        expected_fp17o = {
            'Open': 0,
            'Oldest unsent': None
        }
        self.assertEqual(
            ctx["summary"]["FP17O current tax year"],
            expected_fp17o
        )
        expected_all_time_fp17 = {
            'Oldest unsent': datetime.date.today(),
            'Open': 0,
            'Rejected by compass': 1
        }
        self.assertEqual(
            ctx["summary"]["FP17 all time"],
            expected_all_time_fp17
        )

        self.assertEqual(
            ctx["summary"]["FP17O all time"],
            expected_fp17o
        )

        self.assertTrue(ctx["title"].startswith("Odonto response information for"))
        self.assertTrue(ctx["title"].endswith("NEEDS INVESTIGATION"))

    def test_clean_episodes_episode_succeeded(self, logger, render_to_string, send_mail):
        episode = self.get_episode()
        self.get_submission(episode, Submission.SUCCESS)
        episode.episodesbeinginvestigated_set.create()
        send_report.clean_episodes_being_investigated()
        self.assertEqual(Episode.objects.get().id, episode.id)
        self.assertFalse(EpisodesBeingInvestigated.objects.exists())

    def test_clean_episodes_episode_failed(self, logger, render_to_string, send_mail):
        episode = self.get_episode()
        self.get_submission(episode, Submission.REJECTED_BY_COMPASS)
        episode.episodesbeinginvestigated_set.create()
        send_report.clean_episodes_being_investigated()
        self.assertEqual(Episode.objects.get().id, episode.id)
        self.assertEqual(
            EpisodesBeingInvestigated.objects.get().episode_id, episode.id
        )
