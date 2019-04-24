import datetime
import requests
import logging
from django.conf import settings
URL = "https://ebusiness.dpb.nhs.uk/claimsrequests.asp"


def send_message(xml):
    logging.info(
        "message sent {} {}".format(
            xml, datetime.datetime.now()
        )
    )
    if settings.DEBUG:
        logging.info("NOT SENDING MESSAGE BECAUSE DEBUG=TRUE")
    else:
        result = requests.post(URL, data=xml)
        logging.info(
            "result {} {}".format(
                result.status_code, result.contents
            )
        )

