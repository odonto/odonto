import datetime
from unittest import mock
from django.utils import timezone
from opal.core.test import OpalTestCase
from opal.models import Episode
from odonto.odonto_submissions.models import Submission
from odonto.episode_categories import FP17Episode, FP17OEpisode


class FP17EpisodeTestCase(OpalTestCase):
    def setUp(self):
        self.yesterday_dt = timezone.now() - datetime.timedelta(1)
        self.yesterday = self.yesterday_dt.date()

    def get_episode(self):
        _, episode = self.new_patient_and_episode_please()
        episode.category_name = FP17Episode.display_name
        episode.stage = FP17Episode.SUBMITTED
        episode.save()
        return episode

    def get_submission(self, episode, state):
        mock_str = "odonto.odonto_submissions.models.serializers.\
translate_episode_to_xml"
        with mock.patch(mock_str) as m:
            m.return_value = ""
            submission = Submission.create(episode)
        submission.state = state
        submission.save()
        return submission

    def test_submission_none(self):
        episode = self.get_episode()
        self.assertIsNone(episode.category.submission())

    def test_submission_simple_success(self):
        episode = self.get_episode()
        submission = self.get_submission(episode, Submission.SUCCESS)
        self.assertEqual(episode.category.submission(), submission)

    def test_submission_simple_manually_processed(self):
        episode = self.get_episode()
        submission = self.get_submission(episode, Submission.MANUALLY_PROCESSED)
        self.assertEqual(episode.category.submission(), submission)

    def test_submission_correct_rejection(self):
        episode = self.get_episode()
        submission = self.get_submission(episode, Submission.REJECTED_BY_COMPASS)
        self.assertEqual(episode.category.submission(), submission)

    def test_submission_success_even_when_rejected(self):
        episode = self.get_episode()
        successful_submission = self.get_submission(episode, Submission.SUCCESS)
        successful_submission.created = self.yesterday_dt
        successful_submission.save()

        self.get_submission(episode, Submission.REJECTED_BY_COMPASS)

        self.assertEqual(episode.category.submission(), successful_submission)

    def test_get_successful_episodes(self):
        successful_episode = self.get_episode()
        self.get_submission(successful_episode, Submission.SUCCESS)
        rejected_episode = self.get_episode()
        self.get_submission(rejected_episode, Submission.REJECTED_BY_COMPASS)
        self.assertEqual(
            FP17Episode.get_successful_episodes().get(), successful_episode
        )

    def test_get_successful_episodes_with_manually_processed(self):
        successful_episode = self.get_episode()
        self.get_submission(successful_episode, Submission.MANUALLY_PROCESSED)
        rejected_episode = self.get_episode()
        self.get_submission(rejected_episode, Submission.REJECTED_BY_COMPASS)
        self.assertEqual(
            FP17Episode.get_successful_episodes().get(), successful_episode
        )

    def test_get_successful_episodes_previously_rejected(self):
        episode = self.get_episode()
        rejected = self.get_submission(episode, Submission.REJECTED_BY_COMPASS)
        rejected.created = self.yesterday_dt
        rejected.save()

        self.get_submission(episode, Submission.SUCCESS)
        self.assertEqual(FP17Episode.get_successful_episodes().get(), episode)

    def test_get_rejected_episodes(self):
        """
        Should ignore those have been rejected but have subsequently been
        successful
        """
        successful_episode = self.get_episode()
        self.get_submission(successful_episode, Submission.REJECTED_BY_COMPASS)
        self.get_submission(successful_episode, Submission.SUCCESS)

        rejected_episode = self.get_episode()
        self.get_submission(rejected_episode, Submission.REJECTED_BY_COMPASS)

        self.assertEqual(FP17Episode.get_rejected_episodes().get(), rejected_episode)

    def test_get_episodes_by_rejection_uses_last_rejection(self):
        rejected_episode = self.get_episode()
        rejected_submission = self.get_submission(
            rejected_episode, Submission.REJECTED_BY_COMPASS
        )
        rejected_submission.created = self.yesterday_dt
        rejected_submission.rejection = "not this"
        rejected_submission.save()

        rejected_submission = self.get_submission(
            rejected_episode, Submission.REJECTED_BY_COMPASS
        )
        rejected_submission.rejection = "yes this"
        rejected_submission.save()

        rejection_to_episode = FP17Episode.get_episodes_by_rejection()

        self.assertEqual(len(rejection_to_episode.keys()), 1)

        self.assertEqual(rejection_to_episode["yes this"].get(), rejected_episode)

    def test_get_episodes_by_rejection_ignores_successful(self):
        rejected_episode = self.get_episode()
        rejected_submission = self.get_submission(
            rejected_episode, Submission.REJECTED_BY_COMPASS
        )
        rejected_submission.rejection = "boom"
        rejected_submission.save()

        successful_episode = self.get_episode()
        self.get_submission(successful_episode, Submission.SUCCESS)
        rejection_to_episode = FP17Episode.get_episodes_by_rejection()
        self.assertEqual(len(rejection_to_episode.keys()), 1)
        self.assertEqual(rejection_to_episode["boom"].get(), rejected_episode)

    def test_get_episodes_by_rejection_none(self):
        rejection_to_episode = FP17Episode.get_episodes_by_rejection()
        self.assertEqual(len(rejection_to_episode.keys()), 0)

    def test_get_oldest_unsent_not_submitted(self):
        episode = self.get_episode()
        episode.fp17incompletetreatment_set.update(
            completion_or_last_visit=self.yesterday
        )
        self.assertEqual(FP17Episode.get_oldest_unsent(), episode)

    def test_get_oldest_unsent_not_failed(self):
        episode = self.get_episode()
        episode.fp17incompletetreatment_set.update(
            completion_or_last_visit=self.yesterday
        )
        self.get_submission(episode, Submission.REJECTED_BY_COMPASS)
        self.assertEqual(FP17Episode.get_oldest_unsent(), episode)

    def test_get_oldest_unsent_none(self):
        episode = self.get_episode()
        episode.fp17incompletetreatment_set.update(
            completion_or_last_visit=self.yesterday
        )
        self.get_submission(episode, Submission.SUCCESS)
        self.assertIsNone(FP17Episode.get_oldest_unsent())

    def test_get_sign_off_date(self):
        episode = self.get_episode()
        episode.fp17incompletetreatment_set.update(
            completion_or_last_visit=self.yesterday
        )
        self.assertEqual(episode.category.get_sign_off_date(), self.yesterday)

    def test_summary_rejected(self):
        episode = self.get_episode()
        episode.fp17incompletetreatment_set.update(
            completion_or_last_visit=self.yesterday
        )
        self.get_submission(episode, Submission.REJECTED_BY_COMPASS)
        expected = {
            "Open": 0,
            "Oldest unsent": self.yesterday,
            Submission.REJECTED_BY_COMPASS: 1
        }
        self.assertEqual(
            expected, FP17Episode.summary()
        )

    def test_summary_open(self):
        episode = self.get_episode()
        episode.stage = FP17Episode.OPEN
        episode.save()

        self.get_submission(episode, Submission.REJECTED_BY_COMPASS)
        expected = {
            "Open": 1,
            "Oldest unsent": None,
        }
        self.assertEqual(
            expected, FP17Episode.summary()
        )

    def test_get_submit_link(self):
        episode = self.get_episode()
        l = f"http://ntghcomdent1/pathway/#/fp17-submit/{episode.patient.id}/{episode.id}"
        self.assertEqual(episode.category.get_submit_link(), l)

    def test_get_edit_link(self):
        episode = self.get_episode()
        l = f"http://ntghcomdent1/pathway/#/fp17-edit/{episode.patient.id}/{episode.id}"
        self.assertEqual(episode.category.get_edit_link(), l)


class FP17OEpisodeTestCase(OpalTestCase):
    def setUp(self):
        # this episode should never be found
        _, self.open_episode = self.new_patient_and_episode_please()

        # this episode
        self.open_episode.category_name = FP17OEpisode.display_name
        self.open_episode.stage = FP17OEpisode.OPEN
        self.open_episode.save()
        self.today = datetime.date.today()

    def test_no_unsubmitted_episodes(self):
        self.assertFalse(FP17OEpisode.get_unsubmitted(Episode.objects.all()).exists())

    def test_get_unsubmitted(self):
        _, episode = self.new_patient_and_episode_please()
        episode.category_name = FP17OEpisode.display_name
        episode.stage = FP17OEpisode.OPEN
        episode.save()
        episode.orthodonticassessment_set.update(date_of_assessment=self.today)
        self.assertEqual(
            FP17OEpisode.get_unsubmitted(Episode.objects.all()).get(), episode
        )

    def test_get_sign_off_date_date_of_assessment(self):
        _, episode = self.new_patient_and_episode_please()
        episode.category_name = FP17OEpisode.display_name
        episode.stage = FP17OEpisode.OPEN
        episode.save()
        episode.orthodonticassessment_set.update(date_of_assessment=self.today)
        self.assertEqual(episode.category.get_sign_off_date(), self.today)

    def test_get_sign_off_date_date_of_appliance_fitted(self):
        _, episode = self.new_patient_and_episode_please()
        episode.category_name = FP17OEpisode.display_name
        episode.stage = FP17OEpisode.OPEN
        episode.save()
        episode.orthodonticassessment_set.update(date_of_appliance_fitted=self.today)
        self.assertEqual(episode.category.get_sign_off_date(), self.today)

    def test_get_sign_off_date_date_of_completion(self):
        _, episode = self.new_patient_and_episode_please()
        episode.category_name = FP17OEpisode.display_name
        episode.stage = FP17OEpisode.OPEN
        episode.save()
        episode.orthodontictreatment_set.update(date_of_completion=self.today)
        self.assertEqual(episode.category.get_sign_off_date(), self.today)

    def test_get_submit_link(self):
        episode = self.open_episode
        l = f"http://ntghcomdent1/pathway/#/fp17-o-submit/{episode.patient.id}/{episode.id}"
        self.assertEqual(episode.category.get_submit_link(), l)

    def test_get_edit_link(self):
        episode = self.open_episode
        l = f"http://ntghcomdent1/pathway/#/fp17-o-edit/{episode.patient.id}/{episode.id}"
        self.assertEqual(episode.category.get_edit_link(), l)
