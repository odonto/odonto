import datetime
from importlib import reload
from django.test import override_settings
from unittest import mock
from opal.core.test import OpalTestCase
from odonto.odonto_submissions import dpb_api


@mock.patch("odonto.odonto_submissions.dpb_api.datetime")
@mock.patch("odonto.odonto_submissions.dpb_api.requests.get")
@mock.patch("odonto.odonto_submissions.dpb_api.os.path.exists")
@mock.patch("odonto.odonto_submissions.dpb_api.logger")
class DpbApiTestCase(OpalTestCase):
    @override_settings(SEND_MESSAGES=True, PROJECT_PATH="my_project")
    def test_get_responses(self, logger, os_exists, get, dt):
        dt.datetime.now.return_value = datetime.datetime(2019, 11, 10, 9, 8)
        os_exists.side_effect = [True, False]
        with mock.patch(
            "odonto.odonto_submissions.dpb_api.open", mock.mock_open(), create=True
        ) as m:
            get.return_value.text = "job done"
            result = dpb_api.get_responses()
            self.assertEqual(result, "job done")
            expected_file_name = (
                "my_project/../../responses/responses-10-11-19-09-08.xml"
            )
            m.assert_called_once_with(expected_file_name, "w")
            m.return_value.write.assert_called_once_with("job done")

    @override_settings(SEND_MESSAGES=False, PROJECT_PATH="my_project")
    def test_send_messages_false(self, logger, os_exists, get, dt):
        dt.datetime.now.return_value = datetime.datetime(2019, 11, 10, 9, 8)
        with mock.patch(
            "odonto.odonto_submissions.dpb_api.open", mock.mock_open(), create=True
        ) as m:
            get.return_value.text = "job done"
            result = dpb_api.get_responses()
        self.assertFalse(get.called)
        self.assertFalse(m.called)
        self.assertEqual(result, "SEND_MESSAGES=False: responses not requested")

    @override_settings(SEND_MESSAGES=True, PROJECT_PATH="my_project")
    def test_response_fails(self, logger, os_exists, get, dt):
        dt.datetime.now.return_value = datetime.datetime(2019, 11, 10, 9, 8)
        with mock.patch(
            "odonto.odonto_submissions.dpb_api.open", mock.mock_open(), create=True
        ):
            get.return_value.ok = False
            get.return_value.text = "job failed"
            with self.assertRaises(ValueError):
                dpb_api.get_responses()

            self.assertEqual(logger.info.call_args_list[0][0][0], "getting responses")

            self.assertEqual(
                logger.info.call_args_list[1][0][0],
                "Response is not ok, with 'job failed'",
            )

    @override_settings(SEND_MESSAGES=True, PROJECT_PATH="my_project")
    def test_write_file_already_exists(self, logger, os_exists, get, dt):
        dt.datetime.now.return_value = datetime.datetime(2019, 11, 10, 9, 8)
        os_exists.side_effect = [True, True]
        with mock.patch(
            "odonto.odonto_submissions.dpb_api.open", mock.mock_open(), create=True
        ):
            get.return_value.text = "job done"
            with self.assertRaises(ValueError) as e:
                dpb_api.get_responses()

            self.assertEqual(
                str(e.exception),
                "File my_project/../../responses/responses-10-11-19-09-08.xml already exists",
            )
