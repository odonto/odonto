import datetime
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
            submission.serial_number, 1
        )
        self.assertEqual(
            submission.claim.reference_number, 1
        )

    def test_create_second(self, translate_episode_to_xml, send_message):
        """
        Testing the second submission of the same episode.

        order of circumastances we are testing.

        1. we send down the initial submission
        2. we send down a submission for a different episode
        3. we send down a second submission

        We expect

        The second submission to have a claim of 3 (as its the third message)
        It should have a serial number of 2 (as its the second submission for the
        episode)
        """
        translate_episode_to_xml.return_value = "some_xml"

        # intital submission
        models.Submission.create(self.episode)
        _, other_episode = self.new_patient_and_episode_please()

        # other submission
        models.Submission.create(other_episode)

        submission = models.Submission.create(self.episode)
        self.assertEqual(
            submission.serial_number, 2
        )
        self.assertEqual(
            submission.claim.reference_number,
            models.SystemClaim.objects.order_by(
                "reference_number"
            ).last().reference_number
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

    def test_episode_claim_id_for_second_submission(
        self, translate_episode_to_xml, send_message
    ):
        # should use claim id rather than episode id
        # we create another claim so that claim.id !== episode.id
        models.SystemClaim.create()

        translate_episode_to_xml.return_value = "some_xml"
        first_submission = models.Submission.create(self.episode)
        first_submission.created = datetime.date(2018, 1, 1)
        first_submission.save()
        models.Submission.create(self.episode)
        models.Submission.create(self.episode)

        latest_claim_number = models.SystemClaim.objects.order_by(
            "-reference_number"
        )[0].reference_number
        call_args = list(translate_episode_to_xml.call_args_list[-1][0])
        self.assertEqual(
            call_args,
            [
                self.episode,
                first_submission.claim.reference_number,
                3,
                latest_claim_number,
            ]
        )

    def test_episode_claim_id_where_no_previous_submission(
        self, translate_episode_to_xml, send_message
    ):
        translate_episode_to_xml.return_value = "some_xml"
        models.Submission.create(self.episode)

        latest_claim_number = models.SystemClaim.objects.order_by(
            "-reference_number"
        )[0].reference_number
        call_args = list(translate_episode_to_xml.call_args_list[-1][0])
        self.assertEqual(
            call_args,
            [
                self.episode,
                self.episode.id,
                1,
                latest_claim_number,
            ]
        )


@mock.patch("odonto.odonto_submissions.dpb_api.get_responses")
class CompassBatchResponseTestCase(OpalTestCase):
    def test_get_success(self, get_responses):
        get_responses.return_value.content = "some response"
        batch_response = models.CompassBatchResponse.get()
        self.assertEqual(batch_response.content, "some response")
        self.assertEqual(
            batch_response.state, models.CompassBatchResponse.SUCCESS
        )

    def test_get_failed(self, get_responses):
        get_responses.side_effect = ValueError("failed")

        with self.assertRaises(ValueError):
            models.CompassBatchResponse.get()

        self.assertEqual(
            models.CompassBatchResponse.objects.last().state,
            models.CompassBatchResponse.FAILED
        )

