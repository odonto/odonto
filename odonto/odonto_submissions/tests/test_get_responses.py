from opal.core.test import OpalTestCase
from unittest.mock import patch
from opal.models import Episode
from odonto.odonto_submissions.models import Submission
from odonto.episode_categories import FP17Episode
from odonto.odonto_submissions.management.commands import get_responses

BASE_STR = "odonto.odonto_submissions.management.commands.get_responses"


@patch(BASE_STR + ".send_mail")
@patch(BASE_STR + ".Response.get")
@patch(BASE_STR + ".render_to_string")
@patch(BASE_STR + ".logger")
class GetResponsesTestCase(OpalTestCase):
    def setUp(self):
        self.cmd = get_responses.Command()

    def get_episode(self):
        _, episode = self.new_patient_and_episode_please()
        episode.category_name = FP17Episode.display_name
        episode.stage = FP17Episode.SUBMITTED
        episode.save()
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

    def test_with_error(self, logger, render_to_string, response_get, send_mail):
        response_get.side_effect = ValueError("boom")
        self.cmd.handle()
        logger.error.assert_called_once_with("Failed to get responses")

    def test_without_none(self, logger, render_to_string, response_get, send_mail):
        response = response_get.return_value
        response.get_successfull_submissions.return_value = Submission.objects.all()
        response.get_rejected_submissions.return_value = {}
        self.cmd.handle()
        ctx = render_to_string.call_args[0][1]
        expected_summary = {
            "FP17 Success": 0,
            "FP17 Rejected": 0,
            "FP17O Success": 0,
            "FP17O Rejected": 0,
        }
        self.assertEqual(ctx["summary"]["Latest response"], expected_summary)
        self.assertTrue(ctx["title"].startswith("Odonto response information for"))

    def test_with_success(self, logger, render_to_string, response_get, send_mail):
        episode = self.get_episode()
        self.get_submission(episode, Submission.SUCCESS)
        response = response_get.return_value
        response.get_successfull_submissions.return_value = Submission.objects.all()
        response.get_rejected_submissions.return_value = {}
        self.cmd.handle()
        ctx = render_to_string.call_args[0][1]
        expected_summary = {
            "FP17 Success": 1,
            "FP17 Rejected": 0,
            "FP17O Success": 0,
            "FP17O Rejected": 0,
        }
        self.assertEqual(ctx["summary"]["Latest response"], expected_summary)
        self.assertTrue(ctx["title"].startswith("Odonto response information for"))

    def test_with_rejection(self, logger, render_to_string, response_get, send_mail):
        episode = self.get_episode()
        self.get_submission(episode, Submission.REJECTED_BY_COMPASS)
        response = response_get.return_value
        response.get_successfull_submissions.return_value = Submission.objects.none()
        response.get_rejected_submissions.return_value = {
            Submission.objects.get(): "fail"
        }
        self.cmd.handle()
        ctx = render_to_string.call_args[0][1]
        expected_summary = {
            "FP17 Success": 0,
            "FP17 Rejected": 1,
            "FP17O Success": 0,
            "FP17O Rejected": 0,
        }
        self.assertEqual(ctx["summary"]["Latest response"], expected_summary)
        self.assertTrue(ctx["title"].startswith("Odonto response information for"))