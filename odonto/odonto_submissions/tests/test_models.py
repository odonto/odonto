import mock
from opal.core.test import OpalTestCase
from .models import Submission


@mock.patch("odonto.odonto_submissions.dpb_api.send_message")
@mock.patch("odonto.odonto_submissions.serializers.translate_episode_to_xml")
class SubmissionTestCase(OpalTestCase):
    def setUp(self):
        _, self.episode = self.new_patient_and_episode_please()
        super().setup()

    def test_create_first(self, translate_episode_to_xml, send_message):
        translate_episode_to_xml.return_value = "some_xml"
        submission = Submission.create(self.episode)
        self.assertEqual(
            submission.raw_xml, "some_xml"
        )
        self.assertEqual(
            submission.serial_number, 1
        )
        self.assertEqual(
            submission.systemclaim.reference_number, 1
        )

    def test_create_second(sel, translate_episode_to_xml, send_message):
        pass

    def test_send_already_sent(self, translate_episode_to_xml, send_message):
        pass

    def test_send_already_succeeded(
        self, translate_episode_to_xml, send_message
    ):
        pass

    def test_send_without_exception(
        self, translate_episode_to_xml, send_message
    ):
        pass

    def test_send_with_exception(self, translate_episode_to_xml, send_message):
        pass