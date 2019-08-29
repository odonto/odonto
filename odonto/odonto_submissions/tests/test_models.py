import datetime
from unittest import mock
from collections import OrderedDict
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


@mock.patch("odonto.odonto_submissions.dpb_api.get_responses")
class CompassBatchResponseGetTestCase(OpalTestCase):
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


class CompassBatchResponseParseTestCase(OpalTestCase):
    EMPTY_MESSAGE = " ".join(
        [
            """b'<receipt schvn="1.0" err="There are no responses waiting""",
            """for site 89651"/>'""",
        ]
    )
    SUCCESS_MESSAGE = " ".join(
        [
            'b\'<icset><ic schvn="1.0" synv="1" ori="A0DPB" dest="89651"',
            'datrel="190730" tim="0203" seq="000009" xmcat="1">\r\n\t\t',
            "\r\n\t\t",
            '<contrl schvn="1.0" ori="89651" dest="A0DPB" seq="000003" accd="1"',
            '/>',
            "r\n\t\t",
            "</ic></icset>\r\n'",
        ]
    )

    REJECTION_MESSAGE = " ".join(
        [

            'b\'<icset>',
            '<ic schvn="1.0" synv="1" ori="A0DPB" dest="89651"',
            'datrel="190725" tim="0155" seq="000005" xmcat="1">',
            '\r\n\t\t',
            '<contrl schvn="1.0" ori="89651" dest="A0DPB" seq="000538"',
            'accd="4"/>\r\n\t\t',
            '<respce schvn="1.0">\r\n\t\t\t',
            '<rsp cno="00000000000000" clrn="000538">\r\n\t\t\t\t',
            '<mstxt rspty="@312">',
            'No significant treatment on an EDI claim',
            '</mstxt>\r\n\t\t\t',
            '</rsp>',
            "\r\n\t\t</respce>\r\n\t</ic></icset>\r\n'"
        ]
    )

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        created_dt = datetime.datetime(2018, 1, 1)
        self.empty_response = models.CompassBatchResponse.objects.create(
            state=models.CompassBatchResponse.SUCCESS,
            content=self.EMPTY_MESSAGE,
            created=created_dt
        )

        self.successful_response = models.CompassBatchResponse.objects.create(
            state=models.CompassBatchResponse.SUCCESS,
            content=self.SUCCESS_MESSAGE,
            created=created_dt
        )

        self.rejected_response = models.CompassBatchResponse.objects.create(
            state=models.CompassBatchResponse.SUCCESS,
            content=self.REJECTION_MESSAGE,
            created=created_dt
        )

        _, episode_1 = self.new_patient_and_episode_please()
        _, episode_2 = self.new_patient_and_episode_please()
        # successful submissions
        self.successful_submission = models.Submission.objects.create(
            state=models.Submission.SENT,
            claim=models.SystemClaim.objects.create(reference_number=3),
            episode=episode_1
        )

        # rejected submissions
        self.rejected_submission = models.Submission.objects.create(
            state=models.Submission.SENT,
            claim=models.SystemClaim.objects.create(reference_number=538),
            episode=episode_2
        )

    def test_content_as_dict(self):
        expected_empty = OrderedDict(
            [
                (
                    "receipt",
                    OrderedDict(
                        [
                            ("@schvn", "1.0"),
                            (
                                "@err",
                                "There are no responses waiting for site 89651"
                            ),
                        ]
                    ),
                )
            ]
        )
        expected_success = OrderedDict(
            [
                (
                    "icset",
                    OrderedDict(
                        [
                            (
                                "ic",
                                OrderedDict(
                                    [
                                        ("@schvn", "1.0"),
                                        ("@synv", "1"),
                                        ("@ori", "A0DPB"),
                                        ("@dest", "89651"),
                                        ("@datrel", "190730"),
                                        ("@tim", "0203"),
                                        ("@seq", "000009"),
                                        ("@xmcat", "1"),
                                        (
                                            "contrl",
                                            OrderedDict(
                                                [
                                                    ("@schvn", "1.0"),
                                                    ("@ori", "89651"),
                                                    ("@dest", "A0DPB"),
                                                    ("@seq", "000003"),
                                                    ("@accd", "1"),
                                                ]
                                            ),
                                        ),
                                        ("#text", "r"),
                                    ]
                                ),
                            )
                        ]
                    ),
                )
            ]
        )
        self.assertEqual(
            self.empty_response.content_as_dict, expected_empty
        )
        self.assertEqual(
            self.successful_response.content_as_dict, expected_success
        )

    def test_is_empty(self):
        self.assertTrue(self.empty_response.is_empty())
        self.assertFalse(self.successful_response.is_empty())
        self.assertFalse(self.rejected_response.is_empty())

    def test_get_all_submissions(self):
        self.assertEqual(
            len(self.empty_response.get_all_submissions()), 0
        )
        self.assertEqual(
            self.successful_response.get_all_submissions().get(),
            self.successful_submission
        )
        self.assertEqual(
            self.rejected_response.get_all_submissions().get(),
            self.rejected_submission
        )

    def test_successful_submissions(self):
        self.assertEqual(
            len(self.empty_response.get_successfull_submissions()), 0
        )
        self.assertEqual(
            self.successful_response.get_successfull_submissions().get(),
            self.successful_submission
        )
        self.assertEqual(
            len(self.rejected_response.get_successfull_submissions()), 0
        )

    def test_rejected_submissions(self):
        self.assertEqual(
            len(self.empty_response.get_rejected_submissions()), 0
        )
        self.assertEqual(
            len(self.successful_response.get_rejected_submissions()), 0
        )
        self.assertEqual(
            self.rejected_response.get_rejected_submissions(),
            {
                self.rejected_submission:
                ['No significant treatment on an EDI claim']
            }
        )

    def test_update_submissions(self):
        self.empty_response.update_submissions()
        self.successful_submission.refresh_from_db()
        self.rejected_submission.refresh_from_db()
        self.assertEqual(
            self.successful_submission.state,
            models.Submission.SENT
        )
        self.assertEqual(
            self.rejected_submission.state,
            models.Submission.SENT
        )

        self.successful_response.update_submissions()
        self.successful_submission.refresh_from_db()
        self.rejected_submission.refresh_from_db()
        self.assertEqual(
            self.successful_submission.state,
            models.Submission.SUCCESS
        )
        self.assertEqual(
            self.rejected_submission.state,
            models.Submission.SENT
        )

        self.rejected_response.update_submissions()
        self.successful_submission.refresh_from_db()
        self.rejected_submission.refresh_from_db()
        self.assertEqual(
            self.successful_submission.state,
            models.Submission.SUCCESS
        )
        self.assertEqual(
            self.rejected_submission.state,
            models.Submission.REJECTED_BY_COMPASS
        )
