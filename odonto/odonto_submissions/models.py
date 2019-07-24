from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import transaction
from opal.models import Episode
from . import dpb_api
from .exceptions import MessageSendingException
from . import serializers
from . import logger


class SystemClaim(models.Model):
    reference_number = models.IntegerField(unique=True)

    @classmethod
    def create(cls):
        instance = cls()
        if not cls.objects.exists():
            instance.reference_number = 1
        else:
            max_number = cls.objects.aggregate(
                number=models.Max("reference_number")
            )["number"] + 1
            instance.reference_number = max_number
        instance.save()
        return instance


class Submission(models.Model):
    # Message is sent but we don't know if its successful
    SENT = "Sent"

    # Message is sent and we've recieved a successful response from compass
    SUCCESS = "Success"

    # We've attempted to send the message but were rejected on the post
    FAILED_TO_SEND = "Failed to send"

    # Message has been sent but rejected by get_responses
    REJECTED_BY_COMPASS = "Rejected by compass"
    STATUS = (
        (SENT, SENT,),
        (SUCCESS, SUCCESS,),
        (FAILED_TO_SEND, FAILED_TO_SEND,),
        (REJECTED_BY_COMPASS, REJECTED_BY_COMPASS,),
    )

    raw_xml = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    serial_number = models.IntegerField(default=1)
    state = models.CharField(
        default="", choices=STATUS, max_length=256
    )

    # the response tha we receive immediatly after we send it
    # NOT the one from the batch process
    response = models.TextField(blank=True, default="")
    claim = models.OneToOneField(
        SystemClaim, blank=True, null=True, on_delete=models.SET_NULL
    )
    episode = models.ForeignKey(
        Episode,
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ('-serial_number',)
        get_latest_by = 'serial_number'
        unique_together = (
            ('episode', 'serial_number'),
        )

    def __str__(self):
        return "pk={0.pk} raw_xml={0.raw_xml!r}".format(self)

    @classmethod
    def create(cls, episode):
        current_submission = episode.submission_set.last()

        if current_submission is None:
            serial_number = 1
        else:
            serial_number = current_submission.serial_number + 1

        claim = SystemClaim.create()

        xml = serializers.translate_episode_to_xml(
            episode,
            serial_number,
            claim.reference_number
        )
        return cls.objects.create(
            raw_xml=xml,
            serial_number=serial_number,
            episode=episode,
            claim=claim
        )

    @classmethod
    def send(cls, episode):
        current_submission = episode.submission_set.last()
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

