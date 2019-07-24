import requests
from django.conf import settings
from requests.auth import HTTPBasicAuth
from .exceptions import MessageSendingException
from . import logger


CLAIMS_URL = "https://ebusiness.dpb.nhs.uk/claims.asp"
RESPONSES_URL = "https://ebusiness.dpb.nhs.uk/responses.asp"


def send_message(xml):
    logger.info(
        "send_message() called with {}".format(
            xml
        )
    )
    if settings.SEND_MESSAGES:
        request_kwargs = {
            "auth": HTTPBasicAuth(settings.DPB_USERNAME, settings.DPB_PASSWORD),
            "data":  xml
        }
        if hasattr(settings, "PROXY"):
            proxy = {
                settings.PROXY["IP"]: settings.PROXY["PORT"]
            }
            request_kwargs["proxies"] = proxy
        result = requests.post(
            CLAIMS_URL, **request_kwargs
        )
        logger.info(
            "result {} {}".format(
                result.status_code, result.content
            )
        )
        if result.status_code != 200:
            err = "Message sending resulted in {result.status_code} and \
{result.content}"
            raise MessageSendingException(err)
        else:
            response = result.content
            logger.info(
                "message sent, received a response of {}".format(response)
            )
            return response
    else:
        logger.info("NOT SENDING MESSAGE BECAUSE SEND_MESSAGES=False")
        return "SEND_MESSAGES=False: not sent"


def get_responses():
    return requests.get(
        RESPONSES_URL,
        auth=HTTPBasicAuth(settings.DPB_USERNAME, settings.DPB_PASSWORD),
    )
