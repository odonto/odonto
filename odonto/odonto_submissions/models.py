import xmltodict
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from django.conf import settings
from opal.models import Episode
from . import dpb_api
from .exceptions import MessageSendingException
from . import serializers
from . import logger


class Transmission(models.Model):
    transmission_id = models.IntegerField(unique=True)

    class Meta:
        ordering = ('-transmission_id',)

    def __str__(self):
        return "id={0.id} transmission id={0.transmission_id}".format(
            self
        )

    @classmethod
    def create(cls):
        instance = cls()
        if not cls.objects.exists():
            instance.transmission_id = 1
        else:
            max_number = cls.objects.aggregate(
                number=models.Max("transmission_id")
            )["number"] + 1
            instance.transmission_id = max_number
        instance.save()
        return instance


class CompassBatchResponse(models.Model):
    """
    This requests and stores everything from the dpb api get_responses method
    """

    SUCCESS = "Success"
    FAILED = "Failed"

    STATUS = (
        (SUCCESS, SUCCESS),
        (FAILED, FAILED),
    )
    created = models.DateTimeField(default=timezone.now)
    content = models.TextField(default="")
    state = models.CharField(
        default="", choices=STATUS, max_length=256
    )

    def __str__(self):
        return "id={0.id} created={0.created} state={0.state}".format(
            self
        )

    @classmethod
    def get(cls):
        batch_response = cls()
        response = None
        try:
            response = dpb_api.get_responses()
            batch_response.content = response
            batch_response.state = cls.SUCCESS
            batch_response.save()
            logger.info("Successfully requested the batch responses")
            return batch_response
        except Exception as e:
            batch_response.state = cls.FAILED
            batch_response.save()
            logger.error(f"Batch response failed with {e}")
            raise

    @cached_property
    def content_as_dict(self):
        """
        This method cleans out the xml and casts the content to a dict
        """
        if not self.content:
            raise ValueError("Content not populated for {} id: {}".format(
                self.__class__, self.id
            ))
        return xmltodict.parse(self.content)

    def is_empty(self):
        if "receipt" in self.content_as_dict:
            err = self.content_as_dict["receipt"]["@err"]
            if err == "There are no responses waiting for site {}".format(
                settings.DPB_SITE_ID
            ):
                return True
            else:
                raise ValueError("Unknown error in {} with {}".format(
                    self.id, self.content_as_dict["receipt"]["@err"]
                ))
        return False

    def get_all_submissions(self):
        """
        All submissions mentioned in this batch response
        """
        if self.is_empty():
            return Submission.objects.none()
        content_as_dict = self.content_as_dict

        parsed_submissions = content_as_dict["icset"]["ic"]["contrl"]

        if not isinstance(parsed_submissions, list):
            transmission_ids = [int(parsed_submissions["@seq"])]
        else:
            transmission_ids = [
                int(i["@seq"]) for i in parsed_submissions
            ]
        return Submission.objects.filter(
            transmission__transmission_id__in=transmission_ids
        )

    def get_rejected_submissions(self):
        """
        Returns a dictionary of failed submissions to error message
        """
        result = {}

        # no submissions were mentioned in this message
        if self.is_empty():
            return {}

        # no submissions were rejected
        if "respce" not in self.content_as_dict["icset"]["ic"]:
            return {}

        responses = self.content_as_dict["icset"]["ic"]["respce"]
        if not isinstance(responses, list):
            responses = [responses]
        for i in responses:
            response = i["rsp"]
            submission = self.get_all_submissions().filter(
                transmission__transmission_id=int(response["@clrn"])
            ).get()

            if isinstance(response["mstxt"], list):
                result[submission] = ", ".join([
                    y["#text"] for y in response["mstxt"]
                ])
            else:
                result[submission] = response["mstxt"]["#text"]
        return result

    def get_successfull_submissions(self):
        """
        Returns all successful submissions in this response
        """
        if self.is_empty():
            return Submission.objects.none()
        rejected_submissions = self.get_rejected_submissions()
        return self.get_all_submissions().exclude(
            id__in=[i.id for i in rejected_submissions.keys()]
        )

    def update_submissions(self):
        """
        Updates the state of all submissions mentioned in this response
        """
        successful_submissions = self.get_successfull_submissions()
        successful_submissions.update(state=Submission.SUCCESS)
        self.submission_set.add(*successful_submissions)
        rejected_submissions_to_reasons = self.get_rejected_submissions()
        rejected_submissions = Submission.objects.filter(
            id__in=[i.id for i in rejected_submissions_to_reasons.keys()]
        )
        for rejected_submission in rejected_submissions:
            rejected_submission.rejection = rejected_submissions_to_reasons[
                rejected_submission
            ]
            rejected_submission.state = Submission.REJECTED_BY_COMPASS
            rejected_submission.save()

        self.submission_set.add(*rejected_submissions)


class Submission(models.Model):
    # Message is sent but we are waiting on a response message
    SENT = "Sent"

    # Message is sent and we've received a successful response from Compass
    SUCCESS = "Success"

    # We've attempted to send the message but the POST request failed
    FAILED_TO_SEND = "Failed to send"

    # Message has been sent, a response collected, it was rejected by Compass
    REJECTED_BY_COMPASS = "Rejected by compass"
    STATUS = (
        (SENT, SENT,),
        (SUCCESS, SUCCESS,),
        (FAILED_TO_SEND, FAILED_TO_SEND,),
        (REJECTED_BY_COMPASS, REJECTED_BY_COMPASS,),
    )

    raw_xml = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    submission_count = models.IntegerField(default=1)
    state = models.CharField(
        default="", choices=STATUS, max_length=256
    )

    # The response tha we receive immediately after we send it
    # NOT the one from the batch process
    response = models.TextField(blank=True, default="")

    rejection = models.TextField(blank=True, default="")

    transmission = models.ForeignKey(
        Transmission, blank=True, null=True, on_delete=models.SET_NULL
    )
    episode = models.ForeignKey(
        Episode,
        on_delete=models.CASCADE
    )
    compass_response = models.ForeignKey(
        "CompassBatchResponse",
        null=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        ordering = ('-submission_count',)
        get_latest_by = 'submission_count'
        unique_together = (
            ('episode', 'submission_count'),
        )

    def __str__(self):
        return "pk={0.pk} raw_xml={0.raw_xml!r}".format(self)

    @classmethod
    def create(cls, episode):
        current_submission = episode.submission_set.first()
        # Claim needs to be incrememted each time
        transmission = Transmission.create()

        if current_submission is None:
            submission_count = 1
        else:
            submission_count = current_submission.submission_count + 1

        xml = serializers.translate_episode_to_xml(
            episode,
            submission_count,
            transmission.transmission_id
        )
        return cls.objects.create(
            raw_xml=xml,
            submission_count=submission_count,
            episode=episode,
            transmission=transmission
        )

    @classmethod
    def send(cls, episode):
        current_submission = episode.submission_set.first()
        if current_submission and current_submission.state == cls.SENT:
            ex = "We have a submission with state {} ie awaiting a response \
from compass for submission {} not sending"
            raise MessageSendingException(ex.format(
                cls.SENT, current_submission.id
            ))

        if current_submission and current_submission.state == cls.SUCCESS:
            ex = "We have a submission with state {} ie successfully submitted \
to compass for submission {} not sending"
            raise MessageSendingException(ex.format(
                cls.SUCCESS, current_submission.id
            ))

        new_submission = cls.create(episode)

        try:
            new_submission.response = dpb_api.send_message(
                new_submission.raw_xml
            )
            new_submission.state = cls.SENT
            logger.info("Submission for {} has been sent".format(
                episode
            ))
            new_submission.save()
        except Exception:
            new_submission.state = cls.FAILED_TO_SEND
            logger.error("Submission for {} has failed".format(
                episode
            ))
            new_submission.save()
            raise
        return new_submission

    def get_rejection_reason(self):
        if not self.STATUS == self.REJECTED_BY_COMPASS:
            raise ValueError(
                "Submission {} has not been rejected".format(self.id)
            )
        return self.response.rejected_submissions()[self.id]
