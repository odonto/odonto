import datetime
import requests
from django.conf import settings
from requests.auth import HTTPBasicAuth
from .exceptions import MessageSentException
from . import logger


CLAIMS_URL = "https://ebusiness.dpb.nhs.uk/claims.asp"
RESPONSES_URL = "https://ebusiness.dpb.nhs.uk/responses.asp"


def send_message(xml):
    logger.info(
        "message sent {} {}".format(
            xml, datetime.datetime.now()
        )
    )
    if settings.SEND_MESSAGES or not settings.DEBUG:
        result = requests.post(
            CLAIMS_URL,
            auth=HTTPBasicAuth(settings.DPB_USERNAME, settings.DPB_PASSWORD),
            data=xml
        )
        logger.info(
            "result {} {}".format(
                result.status_code, result.content
            )
        )
        if result.status_code != 200:
            err = "Message sending resulted in {result.status_code} and \
{result.content}"
            raise MessageSentException(err)
        else:
            return result.content
    else:
        logger.info("NOT SENDING MESSAGE BECAUSE DEBUG=TRUE")
        return "DEBUG mode: not sent"


def get_responses():
    return requests.get(
        RESPONSES_URL,
        auth=HTTPBasicAuth(settings.DPB_USERNAME, settings.DPB_PASSWORD),
    )