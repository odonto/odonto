import datetime
import requests
import logging
from django.conf import settings
from requests.auth import HTTPBasicAuth
from .exceptions import MessageSentException


URL = "https://ebusiness.dpb.nhs.uk/claims.asp"


def send_message(xml):
    logging.info(
        "message sent {} {}".format(
            xml, datetime.datetime.now()
        )
    )
    if getattr(settings, "SEND_MESSAGES") or not settings.DEBUG:
        result = requests.post(
            URL,
            auth=HTTPBasicAuth(settings.DPB_USERNAME, settings.DPB_PASSWORD),
            data=xml
        )
        logging.info(
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
        logging.info("NOT SENDING MESSAGE BECAUSE DEBUG=TRUE")
        return "DEBUG mode: not sent"
