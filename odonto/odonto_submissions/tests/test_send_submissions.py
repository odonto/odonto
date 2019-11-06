import datetime
from unittest.mock import patch
from django.test import override_settings
from opal.core.test import OpalTestCase
from opal.models import Episode
from odonto.episode_categories import FP17Episode, FP17OEpisode
from odonto.odonto_submissions.management.commands import send_submissions

BASE_STR = "odonto.odonto_submissions.management.commands.send_submissions"


@patch(BASE_STR + ".send_mail")
@patch(BASE_STR + ".models.Submission.send")
@patch(BASE_STR + ".render_to_string")
@patch(BASE_STR + ".logger")
class SendSubmissionTestCase(OpalTestCase):
    def setUp(self):
        self.cmd = send_submissions.Command()
        self.patient, self.episode = self.new_patient_and_episode_please()
        self.episode.stage = "Submitted"
        self.episode.save()
        self.today = datetime.date.today()
        self.yesterday = self.today - datetime.timedelta(1)

    def test_success_fp17(self, logger, render_to_string, send_submission, send_email):
        Episode.objects.update(category_name=FP17Episode.display_name)
        self.cmd.handle()
        ctx = render_to_string.call_args[0][1]
        self.assertFalse(ctx["threshold_breached"])
        self.assertEqual(ctx["total_success"], 1)
        self.assertEqual(ctx["total_failure"], 0)
        self.assertEqual(ctx["fp17_success_count"], 1)
        self.assertEqual(ctx["fp17_failure_count"], 0)
        self.assertEqual(ctx["fp17o_success_count"], 0)
        self.assertEqual(ctx["fp17o_failure_count"], 0)
        self.assertFalse(ctx["title"].startswith("Urgent"))

    def test_fail_fp17(self, logger, render_to_string, send_submission, send_email):
        send_submission.side_effect = ValueError("boom")
        Episode.objects.update(category_name=FP17Episode.display_name)
        self.cmd.handle()
        ctx = render_to_string.call_args[0][1]
        self.assertFalse(ctx["threshold_breached"])
        self.assertEqual(ctx["total_success"], 0)
        self.assertEqual(ctx["total_failure"], 1)
        self.assertEqual(ctx["fp17_success_count"], 0)
        self.assertEqual(ctx["fp17_failure_count"], 1)
        self.assertEqual(ctx["fp17o_success_count"], 0)
        self.assertEqual(ctx["fp17o_failure_count"], 0)

    def test_success_fp17o(self, logger, render_to_string, send_submission, send_email):
        self.episode.category_name = FP17OEpisode.display_name
        self.episode.save()
        self.patient.demographics_set.update(ethnicity_fk_id=1)
        self.episode.orthodonticassessment_set.update(
            date_of_referral=self.yesterday, date_of_assessment=self.today
        )
        Episode.objects.update(category_name=FP17OEpisode.display_name)
        self.cmd.handle()
        ctx = render_to_string.call_args[0][1]
        self.assertFalse(ctx["threshold_breached"])
        self.assertEqual(ctx["total_success"], 1)
        self.assertEqual(ctx["total_failure"], 0)
        self.assertEqual(ctx["fp17_success_count"], 0)
        self.assertEqual(ctx["fp17_failure_count"], 0)
        self.assertEqual(ctx["fp17o_success_count"], 1)
        self.assertEqual(ctx["fp17o_failure_count"], 0)

    def test_fail_fp17o(self, logger, render_to_string, send_submission, send_email):
        send_submission.side_effect = ValueError("boom")
        self.episode.category_name = FP17OEpisode.display_name
        self.episode.save()
        self.patient.demographics_set.update(ethnicity_fk_id=1)
        self.episode.orthodonticassessment_set.update(
            date_of_referral=self.yesterday, date_of_assessment=self.today
        )
        Episode.objects.update(category_name=FP17OEpisode.display_name)
        self.cmd.handle()
        ctx = render_to_string.call_args[0][1]
        self.assertFalse(ctx["threshold_breached"])
        self.assertEqual(ctx["total_success"], 0)
        self.assertEqual(ctx["total_failure"], 1)
        self.assertEqual(ctx["fp17_success_count"], 0)
        self.assertEqual(ctx["fp17_failure_count"], 0)
        self.assertEqual(ctx["fp17o_success_count"], 0)
        self.assertEqual(ctx["fp17o_failure_count"], 1)

    def test_ignores_some_fp17o(
        self, logger, render_to_string, send_submission, send_email
    ):
        send_submission.side_effect = ValueError("boom")
        self.episode.category_name = FP17OEpisode.display_name
        self.episode.save()
        self.patient.demographics_set.update(ethnicity_fk_id=1)
        Episode.objects.update(category_name=FP17OEpisode.display_name)
        self.cmd.handle()
        ctx = render_to_string.call_args[0][1]
        self.assertFalse(ctx["threshold_breached"])
        self.assertEqual(ctx["total_success"], 0)
        self.assertEqual(ctx["total_failure"], 0)
        self.assertEqual(ctx["fp17_success_count"], 0)
        self.assertEqual(ctx["fp17_failure_count"], 0)
        self.assertEqual(ctx["fp17o_success_count"], 0)
        self.assertEqual(ctx["fp17o_failure_count"], 0)

    @override_settings(FAILED_TO_SEND_WARNING_THRESHOLD=0)
    def test_threshold_breached(
        self, logger, render_to_string, send_submission, send_email
    ):
        send_submission.side_effect = ValueError("boom")
        Episode.objects.update(category_name=FP17Episode.display_name)
        self.cmd.handle()
        ctx = render_to_string.call_args[0][1]
        self.assertTrue(ctx["threshold_breached"])
        self.assertEqual(ctx["total_success"], 0)
        self.assertEqual(ctx["total_failure"], 1)
        self.assertEqual(ctx["fp17_success_count"], 0)
        self.assertEqual(ctx["fp17_failure_count"], 1)
        self.assertEqual(ctx["fp17o_success_count"], 0)
        self.assertEqual(ctx["fp17o_failure_count"], 0)
        self.assertTrue(ctx["title"].startswith("URGENT"))

    def test_none(self, logger, render_to_string, send_submission, send_email):
        Episode.objects.all().delete()
        self.assertIsNone(render_to_string.call_args)
