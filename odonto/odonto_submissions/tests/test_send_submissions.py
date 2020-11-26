import datetime
from unittest.mock import patch
from django.test import override_settings
from opal.core.test import OpalTestCase
from opal.models import Episode
from odonto.odonto_submissions import models
from odonto.episode_categories import FP17Episode, FP17OEpisode
from odonto.odonto_submissions.management.commands import send_submissions

BASE_STR = "odonto.odonto_submissions.management.commands.send_submissions"


@patch(BASE_STR + ".send_mail")
@patch(BASE_STR + ".models.Submission.send")
@patch(BASE_STR + ".render_to_string")
@patch(BASE_STR + ".logger")
class SendSubmissionEmailTestCase(OpalTestCase):
    """
    Tests the summary email that get's sent out of everything that
    has been sent downstream
    """
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
        send_submission.assert_called_once_with(self.episode)

    def test_fail_fp17(self, logger, render_to_string, send_submission, send_email):
        send_submission.side_effect = ValueError("boom")
        Episode.objects.update(category_name=FP17Episode.display_name)
        self.cmd.handle()
        send_submission.assert_called_once_with(self.episode)
        self.assertEqual(
            logger.info.call_args_list[1][0][0],
            f"Sending failed for Episode {self.episode.id} with boom"
        )

    def test_success_fp17o(self, logger, render_to_string, send_submission, send_email):
        self.episode.category_name = FP17OEpisode.display_name
        self.episode.save()
        self.patient.demographics_set.update(ethnicity_fk_id=1)
        self.episode.orthodonticassessment_set.update(
            date_of_referral=self.yesterday, date_of_assessment=self.today
        )
        Episode.objects.update(category_name=FP17OEpisode.display_name)
        self.cmd.handle()
        send_submission.assert_called_once_with(self.episode)

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
        self.assertEqual(
            logger.info.call_args_list[1][0][0],
            f"Sending failed for Episode {self.episode.id} with boom"
        )

    def test_none(self, logger, render_to_string, send_submission, send_email):
        Episode.objects.all().delete()
        self.assertFalse(send_submission.called)


class SendSubmissionGetQSTestCase(OpalTestCase):
    """
    Tests that the correct episodes are being sent downstream
    """
    def setUp(self):
        self.cmd = send_submissions.Command()
        self.patient, self.fp17_episode = self.new_patient_and_episode_please()
        today = datetime.date.today()

        # an fp17 episode ready to be submitted
        self.fp17_episode.stage = FP17Episode.SUBMITTED
        self.fp17_episode.category_name = FP17Episode.display_name
        self.fp17_episode.save()

        # an fp17o episode ready to be submitted
        self.fp17o_episode = self.patient.create_episode()
        self.fp17o_episode.stage = FP17OEpisode.SUBMITTED
        self.fp17o_episode.category_name = FP17OEpisode.display_name
        self.fp17o_episode.save()
        self.fp17o_episode.patient.demographics_set.update(
            ethnicity_fk_id=1
        )
        self.fp17o_episode.orthodonticassessment_set.update(
            date_of_assessment=today,
            date_of_referral=today
        )
        self.fp17o_episode.orthodontictreatment_set.update(
            date_of_completion=None
        )

    def test_get_fp17os_success(self):
        self.assertEqual(
            self.cmd.get_fp17os()[0],
            self.fp17o_episode
        )

    def test_get_fp17os_category(self):
        self.fp17o_episode.category_name = FP17Episode.display_name
        self.fp17o_episode.save()
        self.assertEqual(len(self.cmd.get_fp17os()), False)

    def test_get_fp17os_submitted(self):
        self.fp17o_episode.stage = FP17OEpisode.OPEN
        self.fp17o_episode.save()
        self.assertEqual(len(self.cmd.get_fp17os()), False)

    def test_get_fp17_qs_success(self):
        self.assertEqual(
            self.cmd.get_fp17_qs().get(),
            self.fp17_episode
        )

    def test_get_fp17_qs_category(self):
        self.fp17_episode.category_name = FP17OEpisode.display_name
        self.fp17_episode.save()
        self.assertFalse(self.cmd.get_fp17_qs().exists())

    def test_get_fp17_qs_submitted(self):
        self.fp17_episode.stage = FP17OEpisode.OPEN
        self.fp17_episode.save()
        self.assertFalse(self.cmd.get_fp17_qs().exists())


class FilterForNewOrFailedSinceTestCase(OpalTestCase):
    def setUp(self):
        self.cmd = send_submissions.Command()
        self.patient, self.fp17_episode = self.new_patient_and_episode_please()
        self.this_year = datetime.date(2020, 4, 1)
        self.last_year = datetime.date(2019, 4, 1)

        # an fp17 episode ready to be submitted
        self.fp17_episode.stage = FP17Episode.SUBMITTED
        self.fp17_episode.category_name = FP17Episode.display_name
        self.fp17_episode.save()

    def test_return_failed_this_tax_year(self):
        self.fp17_episode.fp17incompletetreatment_set.update(
            completion_or_last_visit=self.this_year
        )
        self.fp17_episode.submission_set.create(
            state=models.Submission.REJECTED_BY_COMPASS
        )
        result = self.cmd.filter_for_new_or_failed_since(
            Episode.objects.all()
        )
        self.assertEqual(
            result, [self.fp17_episode]
        )

    def test_return_episodes_with_no_submissions(self):
        self.fp17_episode.fp17incompletetreatment_set.update(
            completion_or_last_visit=self.this_year
        )
        result = self.cmd.filter_for_new_or_failed_since(
            Episode.objects.all()
        )
        self.assertEqual(
            result, [self.fp17_episode]
        )

    def test_do_not_return_old_episodes(self):
        self.fp17_episode.fp17incompletetreatment_set.update(
            completion_or_last_visit=self.last_year
        )
        self.fp17_episode.submission_set.create(
            state=models.Submission.REJECTED_BY_COMPASS
        )
        result = self.cmd.filter_for_new_or_failed_since(
            Episode.objects.all()
        )
        self.assertEqual(
            result, []
        )

    def test_do_not_return_episodes_already_succeeded(self):
        self.fp17_episode.fp17incompletetreatment_set.update(
            completion_or_last_visit=self.this_year
        )
        self.fp17_episode.submission_set.create(
            state=models.Submission.SUCCESS
        )
        result = self.cmd.filter_for_new_or_failed_since(
            Episode.objects.all()
        )
        self.assertEqual(
            result, []
        )

    def test_with_fp17o(self):
        fp17o_episode = self.patient.create_episode()
        fp17o_episode.stage = FP17OEpisode.SUBMITTED
        fp17o_episode.category_name = FP17OEpisode.display_name
        fp17o_episode.save()
        fp17o_episode.orthodonticassessment_set.update(
            date_of_assessment=self.this_year
        )
        result = self.cmd.filter_for_new_or_failed_since(
            Episode.objects.filter(category_name=FP17OEpisode.display_name)
        )
        self.assertEqual(
            result, [fp17o_episode]
        )

    def test_with_none(self):
        result = self.cmd.filter_for_new_or_failed_since(
            Episode.objects.none()
        )
        self.assertEqual(
            result, []
        )
