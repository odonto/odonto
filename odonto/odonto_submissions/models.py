from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import transaction
from opal.models import Episode
from . import dpb_api
from .exceptions import MessageSendingException


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
    UNSENT = "Unsent"
    SENT = "Sent"
    SUCCESS = "Success"
    FAILURE = "Failure"
    STATUS = (
        (UNSENT, UNSENT,),
        (SENT, SENT,),
        (SUCCESS, SUCCESS,),
        (FAILURE, FAILURE),
    )

    raw_xml = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    serial_number = models.IntegerField(default=1)
    state = models.CharField(
        default=UNSENT, choices=STATUS, max_length=256
    )
    response = models.TextField(blank=True, default="")
    claim = models.OneToOneField(
        SystemClaim, blank=True, null=True, on_delete=models.SET_NULL
    )

    message = models.ForeignKey(
        "BCDS1Message",
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('-serial_number',)
        get_latest_by = 'serial_number'
        unique_together = (
            ('message', 'serial_number'),
        )

    def __str__(self):
        return "pk={0.pk} raw_xml={0.raw_xml!r}".format(self)


class BCDS1Message(models.Model):
    episode = models.ForeignKey(
        Episode,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL
    )

    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('created',)
        get_latest_by = 'created'
        unique_together = (
            ('episode', 'user'),
        )

    def new_submission(self):
        from odonto.odonto_submissions import serializers
        current_submission = self.submission_set.last()

        if current_submission is None:
            serial_number = 1
        else:
            serial_number = current_submission.serial_number + 1

        claim = SystemClaim.create()

        xml = serializers.translate_episode_to_xml(
            self.episode,
            self.user,
            serial_number,
            claim.reference_number
        )
        self.submission_set.create(
            raw_xml=xml,
            serial_number=serial_number,
        )

    @transaction.atomic
    def send(self):
        current_submission = self.submission_set.last()
        if not current_submission:
            raise MessageSendingException(
                "No submission to send, please call create_submission"
            )
        if not current_submission.state == Submission.UNSENT:
            raise MessageSendingException(
                "Please create a new submission with create_submission"
            )
        current_submission.state = Submission.SENT
        current_submission.save()
        dpb_api.send_message(current_submission.xml)

    def __str__(self):
        current_submission = self.submission_set.last()
        return "pk={} episode_id={} {}".format(
            self.id,
            self.episode.id,
            current_submission.state or "No submissions"
        )

