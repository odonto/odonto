from django.db import models
from django.utils import timezone
from django.db import transaction
from opal.models import Episode
from . import dpb_api


class MessageSentException(Exception):
    pass


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

    def __str__(self):
        return "ref num: {}".format(self.reference_number)


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
        episode = self.message.episode
        return "Episode: {} {}, state: {}".format(
            episode.category_name, episode.id, self.state
        )


class BCDS1Message(models.Model):
    episode = models.ForeignKey(
        Episode,
        on_delete=models.CASCADE
    )

    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('created',)
        get_latest_by = 'created'
        verbose_name = "BCDS1 Message"

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
            raise MessageSentException(
                "No submission to send, please call create_submission"
            )
        if not current_submission.state == Submission.UNSENT:
            raise MessageSentException(
                "Please create a new submission with create_submission"
            )
        current_submission.state = Submission.SENT
        current_submission.save()
        # this just tells us that the message has been received
        # messages are processed as part of a batch process
        current_submission.response = dpb_api.send_message(current_submission.raw_xml)
        current_submission.save()

    def __str__(self):
        current_submission = self.submission_set.last()
        if current_submission:
            state = current_submission.state
        else:
            state = "No submissions"

        return "pk={} episode_id={} {}".format(
            self.id,
            self.episode.id,
            state
        )

