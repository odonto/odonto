import requests
import os
import datetime
from django.conf import settings
from requests.auth import HTTPBasicAuth
from .exceptions import MessageSendingException
from . import logger


CLAIMS_URL = "https://ebusiness.dpb.nhs.uk/claims.asp"
RESPONSES_URL = "https://ebusiness.dpb.nhs.uk/responses.asp"


def send_message(xml):
    logger.info("send_message() called with {}".format(xml))
    if settings.SEND_MESSAGES:
        request_kwargs = {
            "auth": HTTPBasicAuth(settings.DPB_USERNAME, settings.DPB_PASSWORD),
            "data": xml,
            "verify": settings.SSH_CERTS
        }
        if hasattr(settings, "PROXY"):
            request_kwargs["proxies"] = settings.PROXY

        result = requests.post(CLAIMS_URL, **request_kwargs)
        logger.info("result {} {}".format(result.status_code, result.content))
        if result.status_code != 200:
            err = "Message sending resulted in {result.status_code} and \
{result.content}"
            raise MessageSendingException(err)
        else:
            response = result.content
            logger.info("message sent, received a response of {}".format(response))
            return response
    else:
        logger.info("NOT SENDING MESSAGE BECAUSE SEND_MESSAGES=False")
        return "SEND_MESSAGES=False: not sent"


def get_responses():
    logger.info("getting responses")
    responses_dir = os.path.join(f"{settings.PROJECT_PATH}", "..", "..", "responses")
    if not os.path.exists(responses_dir):
        raise ValueError(
            f"Unable to get responses as the save dir {responses_dir} does not exist"
        )
    request_kwargs = {
        "auth": HTTPBasicAuth(settings.DPB_USERNAME, settings.DPB_PASSWORD),
        "verify": settings.SSH_CERTS
    }
    if hasattr(settings, "PROXY"):
        request_kwargs["proxies"] = settings.PROXY

    if not settings.SEND_MESSAGES:
        logger.info("NOT REQUESTING RESPONSES BECAUSE SEND_MESSAGES=False")
        return "SEND_MESSAGES=False: responses not requested"

    response = requests.get(RESPONSES_URL, **request_kwargs)

    if response.ok:
        logger.info(f"Responses recieved {response.text}")
        dt = datetime.datetime.now().strftime("%d-%m-%y-%H-%M")
        file_name = os.path.join(responses_dir, f"responses-{dt}.xml")

        if os.path.exists(file_name):
            raise ValueError(f"File {file_name} already exists")

        with open(file_name, "w") as r:
            r.write(response.text)
        return response.text

    logger.info(f"Response is not ok, with '{response.text}'")
    raise ValueError(
        f"Unable to get responses {response.status_code} {response.content}"
    )
