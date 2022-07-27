import datetime
from unittest import mock
from django.utils import timezone
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
            submission.submission_count, 1
        )
        self.assertEqual(
            submission.transmission.transmission_id, 1
        )

    def test_create_second(self, translate_episode_to_xml, send_message):
        """
        Testing the second submission of the same episode.

        order of circumastances we are testing.

        1. we send down the initial submission
        2. we send down a submission for a different episode
        3. we send down a second submission

        We expect

        The second submission to have a transmission of 3 (as its the third message)
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
            submission.submission_count, 2
        )
        self.assertEqual(
            submission.transmission.transmission_id,
            models.Transmission.objects.order_by(
                "transmission_id"
            ).last().transmission_id
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
            submission.request_response, "some response"
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
            submission.request_response, ""
        )
        self.assertEqual(
            submission.state, models.Submission.FAILED_TO_SEND
        )

    def test_send_replace(
        self, translate_episode_to_xml, send_message
    ):
        send_message.return_value = "some response"
        translate_episode_to_xml.return_value = "some_xml"
        sent_submission = models.Submission.send(self.episode, replace=True)
        # refetch the submission to make sure its saved
        submission = models.Submission.objects.get(id=sent_submission.id)
        self.assertEqual(
            submission.request_response, "some response"
        )
        self.assertEqual(
            submission.raw_xml, "some_xml"
        )
        self.assertEqual(
            submission.state, models.Submission.SENT
        )
        self.assertEqual(
            submission.submission_type, models.Submission.REPLACE
        )
        self.assertTrue(
            translate_episode_to_xml.call_args[1]["replace"]
        )
        self.assertFalse(
            translate_episode_to_xml.call_args[1]["delete"]
        )

    @mock.patch("odonto.odonto_submissions.models.has_changed")
    def test_send_replace_successful(
        self, has_changed, translate_episode_to_xml, send_message
    ):
        """
        We should be able to send down an episode with replace (ie updating it)
        even if it has been successfully submitted
        """
        send_message.return_value = "some response"
        translate_episode_to_xml.return_value = "some_xml"
        has_changed.return_value = True
        self.episode.submission_set.create(
            state=models.Submission.SUCCESS
        )

        sent_submission = models.Submission.send(self.episode, replace=True)
        # refetch the submission to make sure its saved
        submission = models.Submission.objects.get(id=sent_submission.id)
        self.assertEqual(
            submission.request_response, "some response"
        )
        self.assertEqual(
            submission.raw_xml, "some_xml"
        )
        self.assertEqual(
            submission.state, models.Submission.SENT
        )
        self.assertEqual(
            submission.submission_type, models.Submission.REPLACE
        )
        self.assertTrue(
            translate_episode_to_xml.call_args[1]["replace"]
        )
        self.assertFalse(
            translate_episode_to_xml.call_args[1]["delete"]
        )

    def test_send_delete(
        self, translate_episode_to_xml, send_message
    ):
        send_message.return_value = "some response"
        translate_episode_to_xml.return_value = "some_xml"
        sent_submission = models.Submission.send(self.episode, delete=True)
        # refetch the submission to make sure its saved
        submission = models.Submission.objects.get(id=sent_submission.id)
        self.assertEqual(
            submission.request_response, "some response"
        )
        self.assertEqual(
            submission.raw_xml, "some_xml"
        )
        self.assertEqual(
            submission.state, models.Submission.SENT
        )
        self.assertEqual(
            submission.submission_type, models.Submission.DELETE
        )
        self.assertFalse(
            translate_episode_to_xml.call_args[1]["replace"]
        )
        self.assertTrue(
            translate_episode_to_xml.call_args[1]["delete"]
        )

    @mock.patch("odonto.odonto_submissions.models.has_changed")
    def test_send_delete_successful(
        self, has_changed, translate_episode_to_xml, send_message
    ):
        """
        We should be able to send down an episode with delete
        even if it has been successfully submitted
        """
        send_message.return_value = "some response"
        translate_episode_to_xml.return_value = "some_xml"
        has_changed.return_value = True
        self.episode.submission_set.create(
            state=models.Submission.SUCCESS
        )

        sent_submission = models.Submission.send(self.episode, delete=True)
        # refetch the submission to make sure its saved
        submission = models.Submission.objects.get(id=sent_submission.id)
        self.assertEqual(
            submission.request_response, "some response"
        )
        self.assertEqual(
            submission.raw_xml, "some_xml"
        )
        self.assertEqual(
            submission.state, models.Submission.SENT
        )
        self.assertEqual(
            submission.submission_type, models.Submission.DELETE
        )
        self.assertFalse(
            translate_episode_to_xml.call_args[1]["replace"]
        )
        self.assertTrue(
            translate_episode_to_xml.call_args[1]["delete"]
        )

    def test_episode_claim_id_for_second_submission(
        self, translate_episode_to_xml, send_message
    ):
        # should use claim id rather than episode id
        # we create another claim so that claim.id !== episode.id
        models.Transmission.create()

        translate_episode_to_xml.return_value = "some_xml"
        first_submission = models.Submission.create(self.episode)
        first_submission.created = timezone.make_aware(datetime.datetime(
            models.SUBMISSION_ID_DATE_CHANGE.year,
            models.SUBMISSION_ID_DATE_CHANGE.month,
            models.SUBMISSION_ID_DATE_CHANGE.day,
            6, 6
        ))

        first_submission.save()
        second_submission = models.Submission.create(self.episode)
        second_submission.created = timezone.make_aware(datetime.datetime(
            models.SUBMISSION_ID_DATE_CHANGE.year,
            models.SUBMISSION_ID_DATE_CHANGE.month,
            models.SUBMISSION_ID_DATE_CHANGE.day,
            7, 6
        ))
        second_submission.save()
        models.Submission.create(self.episode)

        latest_transmission_id = models.Transmission.objects.order_by(
            "-transmission_id"
        )[0].transmission_id
        call_args = list(translate_episode_to_xml.call_args_list[-1][0])
        self.assertEqual(
            call_args,
            [
                self.episode,
                self.episode.id,
                3,
                latest_transmission_id,
            ]
        )

    def test_episode_claim_id_for_second_submission_before_dt_change(
        self, translate_episode_to_xml, send_message
    ):
        # should use claim id rather than episode id
        # we create another claim so that claim.id !== episode.id
        models.Transmission.create()

        translate_episode_to_xml.return_value = "some_xml"
        first_submission = models.Submission.create(self.episode)
        first_submission.created = timezone.make_aware(datetime.datetime(2018, 1, 1))
        first_submission.save()
        models.Submission.create(self.episode)
        models.Submission.create(self.episode)

        latest_transmission_number = models.Transmission.objects.order_by(
            "-transmission_id"
        )[0].transmission_id
        call_args = list(translate_episode_to_xml.call_args_list[-1][0])
        self.assertEqual(
            call_args,
            [
                self.episode,
                first_submission.transmission.transmission_id,
                3,  # should be 3 because there have been 3 submissions
                latest_transmission_number,
            ]
        )

    def test_episode_claim_id_where_no_previous_submission(
        self, translate_episode_to_xml, send_message
    ):
        translate_episode_to_xml.return_value = "some_xml"
        models.Submission.create(self.episode)

        latest_transmission_id = models.Transmission.objects.order_by(
            "-transmission_id"
        )[0].transmission_id
        call_args = list(translate_episode_to_xml.call_args_list[-1][0])
        self.assertEqual(
            call_args,
            [
                self.episode,
                self.episode.id,
                1,
                latest_transmission_id,
            ]
        )


@mock.patch("odonto.odonto_submissions.dpb_api.get_responses")
class ResponseGetTestCase(OpalTestCase):
    def test_get_success(self, get_responses):
        get_responses.return_value = "some response"
        batch_response = models.Response.get()
        self.assertEqual(batch_response.content, "some response")
        self.assertEqual(
            batch_response.state, models.Response.SUCCESS
        )

    def test_get_failed(self, get_responses):
        get_responses.side_effect = ValueError("failed")

        with self.assertRaises(ValueError):
            models.Response.get()

        self.assertEqual(
            models.Response.objects.last().state,
            models.Response.FAILED
        )


class ResponseParseTestCase(OpalTestCase):
    EMPTY_MESSAGE = """
        <receipt schvn="1.0" err="There are no
responses waiting for site 89651"/>
    """

    UNKOWN_ERR = """
        <receipt schvn="1.0" err="Boom for site 89651"/>
    """

    SUCCESS_MESSAGE = """
        <icset><ic schvn="1.0" synv="1" ori="A0DPB" dest="89651"
        datrel="190730" tim="0203" seq="000009" xmcat="1">
        <contrl schvn="1.0" ori="89651" dest="A0DPB" seq="{transmission_id}" accd="1"
        />r
        </ic></icset>
    """

    def get_success_messages(self):
        """
        A successful message, returns the submission and th
        """
        _, episode = self.new_patient_and_episode_please()
        created_dt = timezone.make_aware(datetime.datetime(2019, 12, 1))
        transmission = models.Transmission.objects.create(transmission_id=3)
        successful_submission = models.Submission.objects.create(
            state=models.Submission.SENT,
            transmission=transmission,
            episode=episode
        )
        successful_response = models.Response.objects.create(
            state=models.Response.SUCCESS,
            content=self.SUCCESS_MESSAGE.format(
                transmission_id=transmission.transmission_id
            ),
            created=created_dt
        )
        return dict(
            submission=successful_submission,
            response=successful_response
        )

    MULTIPLE_SUCCESS_MESSAGES = """
        <icset><ic schvn="1.0" synv="1" ori="A0DPB" dest="89651"
        datrel="190730" tim="0203" seq="000009" xmcat="1">
        <contrl schvn="1.0" ori="89651" dest="A0DPB" seq="{transmission_id_1}"
        accd="1" />
        <contrl schvn="1.0" ori="89651" dest="A0DPB" seq="{transmission_id_2}"
        accd="1" />
        </ic></icset>
    """

    def get_multiple_success_messages(self):
        _, episode_1 = self.new_patient_and_episode_please()
        _, episode_2 = self.new_patient_and_episode_please()
        created_dt = timezone.make_aware(datetime.datetime(2019, 12, 1))
        transmission_1 = models.Transmission.objects.create(transmission_id=1)
        successful_submission_1 = models.Submission.objects.create(
            state=models.Submission.SENT,
            transmission=transmission_1,
            episode=episode_1
        )
        transmission_2 = models.Transmission.objects.create(transmission_id=2)
        successful_submission_2 = models.Submission.objects.create(
            state=models.Submission.SENT,
            transmission=transmission_2,
            episode=episode_2
        )

        successful_response = models.Response.objects.create(
            state=models.Response.SUCCESS,
            content=self.MULTIPLE_SUCCESS_MESSAGES.format(
                transmission_id_1=transmission_1.transmission_id,
                transmission_id_2=transmission_2.transmission_id,
            ),
            created=created_dt
        )
        return dict(
            submissions=[successful_submission_1, successful_submission_2],
            response=successful_response
        )

    REJECTION_MESSAGE = """
        <icset>
        <ic schvn="1.0" synv="1" ori="A0DPB" dest="89651"
        datrel="190725" tim="0155" seq="000005" xmcat="1">
        <contrl schvn="1.0" ori="89651" dest="A0DPB" seq="{transmission_id}"
        accd="4"/>
        <respce schvn="1.0">
        <rsp cno="00000000000000" clrn="{submission_id}">
        <mstxt rspty="@312">No significant treatment on an EDI claim
        </mstxt>
        </rsp>
        </respce></ic></icset>
    """

    def get_rejection_messages(self):
        _, episode = self.new_patient_and_episode_please()
        created_dt = timezone.make_aware(datetime.datetime(2019, 12, 1))
        transmission = models.Transmission.objects.create(transmission_id=1)
        submission = models.Submission.objects.create(
            state=models.Submission.SENT,
            transmission=transmission,
            episode=episode,
            created=created_dt
        )
        response = models.Response.objects.create(
            state=models.Response.SUCCESS,
            content=self.REJECTION_MESSAGE.format(
                transmission_id=transmission.transmission_id,
                submission_id=episode.id
            ),
            created=created_dt
        )
        return dict(
            submission=submission,
            response=response
        )

    MULTUPLE_REJECTION_MESSAGE = """
        <icset>
        <ic schvn="1.0" synv="1" ori="A0DPB" dest="89651"
        datrel="190725" tim="0155" seq="000005" xmcat="1">
        <contrl schvn="1.0" ori="89651" dest="A0DPB" seq="{transmission_id}"
        accd="4"/>
        <respce schvn="1.0">
        <rsp cno="00000000000000" clrn="{submission_id}">
        <mstxt rspty="@312">
        No significant treatment on an EDI claim
        </mstxt>s
        <mstxt rspty="870">
        Free Repair/Replacement Within 12 Months invalid
        </mstxt>
        </rsp>
        </respce>
        </ic>
        </icset>
    """

    def get_messages_with_multiple_rejections(self):
        _, episode = self.new_patient_and_episode_please()
        created_dt = timezone.make_aware(datetime.datetime(2019, 12, 1))
        transmission = models.Transmission.objects.create(transmission_id=3)
        submission = models.Submission.objects.create(
            state=models.Submission.SENT,
            transmission=transmission,
            episode=episode
        )
        response = models.Response.objects.create(
            state=models.Response.SUCCESS,
            content=self.MULTUPLE_REJECTION_MESSAGE.format(
                transmission_id=transmission.transmission_id,
                submission_id=episode.id
            ),
            created=created_dt
        )
        return dict(
            submission=submission,
            response=response
        )

    MULTIPLE_REJECTIONS_MESSAGE = """
        <icset>
        <ic schvn="1.0" synv="1" ori="A0DPB" dest="89651"
        datrel="190725" tim="0155" seq="000005" xmcat="1">
        <contrl schvn="1.0" ori="89651" dest="A0DPB" seq="{transmission_id_1}"
        accd="4"/>
        <contrl schvn="1.0" ori="89651" dest="A0DPB" seq="{transmission_id_2}"
        accd="4"/>
        <respce schvn="1.0">
        <rsp cno="00000000000000" clrn="{submission_id_1}">
        <mstxt rspty="@312">
        No significant treatment on an EDI claim
        </mstxt>
        </rsp>
        <rsp cno="00000000000000" clrn="{submission_id_2}">
        <mstxt rspty="870">
        Free Repair/Replacement Within 12 Months invalid
        </mstxt>
        </rsp>
        </respce>
        </ic>
        </icset>
    """

    def get_multiple_rejection_messages(self):
        _, episode_1 = self.new_patient_and_episode_please()
        _, episode_2 = self.new_patient_and_episode_please()
        created_dt = timezone.make_aware(datetime.datetime(2019, 12, 1))
        transmission_1 = models.Transmission.objects.create(transmission_id=1)
        submission_1 = models.Submission.objects.create(
            state=models.Submission.SENT,
            transmission=transmission_1,
            episode=episode_1
        )
        transmission_2 = models.Transmission.objects.create(transmission_id=2)
        submission_2 = models.Submission.objects.create(
            state=models.Submission.SENT,
            transmission=transmission_2,
            episode=episode_2
        )

        response = models.Response.objects.create(
            state=models.Response.SUCCESS,
            content=self.MULTIPLE_REJECTIONS_MESSAGE.format(
                transmission_id_1=transmission_1.transmission_id,
                transmission_id_2=transmission_2.transmission_id,
                submission_id_1=episode_1.id,
                submission_id_2=episode_2.id,
            ),
            created=created_dt
        )
        return dict(
            submissions=[submission_1, submission_2],
            response=response
        )

    COMBINATION_MESSAGE = """
        <icset>
        <ic schvn="1.0" synv="1" ori="A0DPB" dest="89651"
        datrel="190725" tim="0155" seq="000005" xmcat="1">
        <contrl schvn="1.0" ori="89651" dest="A0DPB" seq="{transmission_id_1}"
        accd="1"/>
        <contrl schvn="1.0" ori="89651" dest="A0DPB" seq="{transmission_id_2}" accd="1"
        />
        <respce schvn="1.0">
        <rsp cno="00000000000000" clrn="{submission_id}">
        <mstxt rspty="@312">
        No significant treatment on an EDI claim
        </mstxt>
        </rsp>
        </respce></ic></icset>
    """

    def get_combination_message(self):
        _, episode_1 = self.new_patient_and_episode_please()
        _, episode_2 = self.new_patient_and_episode_please()
        created_dt = timezone.make_aware(datetime.datetime(2019, 12, 1))
        transmission_1 = models.Transmission.objects.create(transmission_id=1)
        submission_1 = models.Submission.objects.create(
            state=models.Submission.SENT,
            transmission=transmission_1,
            episode=episode_1
        )
        transmission_2 = models.Transmission.objects.create(transmission_id=2)
        submission_2 = models.Submission.objects.create(
            state=models.Submission.SENT,
            transmission=transmission_2,
            episode=episode_2
        )

        response = models.Response.objects.create(
            state=models.Response.SUCCESS,
            content=self.COMBINATION_MESSAGE.format(
                transmission_id_1=transmission_1.transmission_id,
                transmission_id_2=transmission_2.transmission_id,
                submission_id=episode_1.id,
            ),
            created=created_dt
        )
        return dict(
            submissions=[submission_1, submission_2],
            response=response
        )

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        created_dt = timezone.make_aware(datetime.datetime(2019, 12, 1))
        self.empty_response = models.Response.objects.create(
            state=models.Response.SUCCESS,
            content=self.EMPTY_MESSAGE,
            created=created_dt
        )

        self.unkown_err = models.Response.objects.create(
            state=models.Response.SUCCESS,
            content=self.UNKOWN_ERR,
            created=created_dt
        )

    def test_update_submissions_empty(self):
        self.empty_response.update_submissions()
        self.assertEqual(
            self.get_success_messages()["submission"].state,
            models.Submission.SENT
        )
        self.assertEqual(
            self.get_rejection_messages()["submission"].state,
            models.Submission.SENT
        )
        self.assertFalse(
            self.empty_response.submission_set.exists()
        )

    def test_update_submissions_success(self):
        successful_messages = self.get_success_messages()
        submission = successful_messages["submission"]
        response = successful_messages["response"]
        self.assertEqual(
            submission.state,
            models.Submission.SENT
        )
        response.update_submissions()
        submission.refresh_from_db()
        self.assertEqual(
            submission.state,
            models.Submission.SUCCESS
        )
        self.assertEqual(
            submission.response,
            response
        )

    def test_update_multipe_submissions_success(self):
        successful_messages = self.get_multiple_success_messages()
        submission_1, submission_2 = successful_messages["submissions"]
        response = successful_messages["response"]
        self.assertEqual(
            submission_1.state,
            models.Submission.SENT
        )
        self.assertEqual(
            submission_2.state,
            models.Submission.SENT
        )
        response.update_submissions()
        submission_1.refresh_from_db()
        submission_2.refresh_from_db()
        self.assertEqual(
            submission_1.state,
            models.Submission.SUCCESS
        )
        self.assertEqual(
            submission_1.response,
            response
        )
        self.assertEqual(
            submission_2.state,
            models.Submission.SUCCESS
        )
        self.assertEqual(
            submission_2.response,
            response
        )

    def test_update_submissions_rejected(self):
        rejection_messages = self.get_rejection_messages()
        submission = rejection_messages["submission"]
        response = rejection_messages["response"]
        self.assertEqual(
            submission.state,
            models.Submission.SENT
        )
        response.update_submissions()
        submission.refresh_from_db()
        self.assertEqual(
            submission.state,
            models.Submission.REJECTED_BY_COMPASS
        )
        self.assertEqual(
            submission.response,
            response
        )
        self.assertEqual(
            submission.rejection,
            "No significant treatment on an EDI claim"
        )

    def test_update_submissions_multiple_rejection_reasons(self):
        rejection_messages = self.get_messages_with_multiple_rejections()
        submission = rejection_messages["submission"]
        response = rejection_messages["response"]
        self.assertEqual(
            submission.state,
            models.Submission.SENT
        )
        response.update_submissions()
        submission.refresh_from_db()
        self.assertEqual(
            submission.state,
            models.Submission.REJECTED_BY_COMPASS
        )
        self.assertEqual(
            submission.response,
            response
        )
        reject_reason = "".join([
            "No significant treatment on an EDI claim, ",
            "Free Repair/Replacement Within 12 Months invalid"
        ])
        self.assertEqual(
            submission.rejection,
            reject_reason
        )

    def test_update_submissions_multiple_rejected_episodes(self):
        rejection_messages = self.get_multiple_rejection_messages()
        response = rejection_messages["response"]
        submission_1, submission_2 = rejection_messages["submissions"]
        self.assertEqual(
            submission_1.state,
            models.Submission.SENT
        )
        self.assertEqual(
            submission_2.state,
            models.Submission.SENT
        )
        response.update_submissions()
        submission_1.refresh_from_db()
        submission_2.refresh_from_db()
        self.assertEqual(
            submission_1.state,
            models.Submission.REJECTED_BY_COMPASS
        )
        self.assertEqual(
            submission_2.state,
            models.Submission.REJECTED_BY_COMPASS
        )
        self.assertEqual(
            submission_1.response,
            response
        )
        self.assertEqual(
            submission_2.response,
            response
        )

        self.assertEqual(
            submission_1.rejection,
            "No significant treatment on an EDI claim"
        )
        self.assertEqual(
            submission_2.rejection,
            "Free Repair/Replacement Within 12 Months invalid"
        )

    def test_update_submission_accepted_and_rejected(self):
        messages = self.get_combination_message()
        response = messages["response"]
        rejected_submission, successful_submission = messages["submissions"]

        response.update_submissions()
        rejected_submission.refresh_from_db()
        self.assertEqual(
            rejected_submission.state,
            models.Submission.REJECTED_BY_COMPASS
        )
        self.assertEqual(
            rejected_submission.response,
            response
        )
        self.assertEqual(
            rejected_submission.rejection,
            "No significant treatment on an EDI claim"
        )

        successful_submission.refresh_from_db()
        self.assertEqual(
            successful_submission.state,
            models.Submission.SUCCESS
        )
        self.assertEqual(
            successful_submission.response,
            response
        )
