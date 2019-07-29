from unittest import mock
from opal.core.test import OpalTestCase
from .. import models
from .. import exceptions


@mock.patch("odonto.odonto_submissions.dpb_api.send_message")
@mock.patch("odonto.odonto_submissions.serializers.translate_episode_to_xml")
class SubmissionTestCase(OpalTestCase):
    def setUp(self):
        _, self.episode = self.new_patient_and_episode_please()
        super().setUp()

    def test_create_first(self, translate_episode_to_xml, send_message):
        translate_episode_to_xml.return_value = "some_xml"
        submission = models.Submission.create(self.episode)
        self.assertEqual(
            submission.raw_xml, "some_xml"
        )
        self.assertEqual(
            submission.submission_number, 1
        )
        self.assertEqual(
            submission.claim.reference_number, 1
        )

    def test_create_second(self, translate_episode_to_xml, send_message):
        """
        Testing the second submission of the same episode.

        We should use a new claim a different submission number
        """
        translate_episode_to_xml.return_value = "some_xml"
        # create an inital submission
        models.Submission.create(self.episode)
        submission = models.Submission.create(self.episode)
        self.assertEqual(
            submission.submission_number, 2
        )
        self.assertEqual(
            submission.claim, models.SystemClaim.objects.last()
        )

    def test_send_already_sent(self, translate_episode_to_xml, send_message):
        translate_episode_to_xml.return_value = "some_xml"
        submission = models.Submission.create(self.episode)
        submission.state = models.Submission.SENT
        submission.save()
        expected = "We have a submission with state {} ie awaiting a response \
from compass for submission {} not sending"
        expected = expected.format(models.Submission.SENT, submission.id)
        with self.assertRaises(exceptions.MessageSendingException) as e:
            models.Submission.send(self.episode)
        self.assertEqual(str(e.exception), expected)

        self.assertFalse(send_message.called)

    def test_send_already_succeeded(
        self, translate_episode_to_xml, send_message
    ):
        translate_episode_to_xml.return_value = "some_xml"
        submission = models.Submission.create(self.episode)
        submission.state = models.Submission.SUCCESS
        submission.save()
        expected = "We have a submission with state {} ie successfully submitted \
to compass for submission {} not sending"
        expected = expected.format(models.Submission.SUCCESS, submission.id)
        with self.assertRaises(exceptions.MessageSendingException) as e:
            models.Submission.send(self.episode)
        self.assertEqual(str(e.exception), expected)
        self.assertFalse(send_message.called)

    def test_send_without_exception(
        self, translate_episode_to_xml, send_message
    ):
        send_message.return_value = "some response"
        translate_episode_to_xml.return_value = "some_xml"
        sent_submission = models.Submission.send(self.episode)
        # refetch the submission to make sure its saved
        submission = models.Submission.objects.get(id=sent_submission.id)
        self.assertEqual(
            submission.response, "some response"
        )
        self.assertEqual(
            submission.raw_xml, "some_xml"
        )
        self.assertEqual(
            submission.state, models.Submission.SENT
        )

    def test_send_with_exception(self, translate_episode_to_xml, send_message):
        send_message.side_effect = exceptions.MessageSendingException("Failed")
        translate_episode_to_xml.return_value = "some_xml"
        with self.assertRaises(exceptions.MessageSendingException) as e:
            models.Submission.send(self.episode)
        # refetch the submission to make sure its saved
        submission = self.episode.submission_set.last()
        self.assertEqual(
            submission.response, ""
        )
        self.assertEqual(
            submission.state, models.Submission.FAILED_TO_SEND
        )


