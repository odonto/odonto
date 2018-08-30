from django.db import models
from django.utils import timezone


class Provider(models.Model):
    name = models.CharField(max_length=255)

    contract_number = models.IntegerField(unique=True)
    provider_number = models.IntegerField(unique=True)

    created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('name',)
        get_latest_by = 'created'

    def __str__(self):
        return "pk={0.pk} name={0.name!r}".format(self)


class Performer(models.Model):
    provider = models.ForeignKey(
        Provider,
        on_delete=models.CASCADE,
        related_name='performers',
    )

    name = models.CharField(max_length=255)

    created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('name',)
        get_latest_by = 'created'

    def __str__(self):
        return "pk={0.pk} title={0.name!r}".format(self)


class BCDS1Message(models.Model):
    provider = models.ForeignKey(
        Provider,
        related_name='bcds1_messages',
    )

    claim_number = models.IntegerField()

    created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('-claim_number',)
        get_latest_by = 'created'

        unique_together = (
            ('provider', 'claim_number'),
        )

    def __str__(self):
        return "pk={0.pk} claim_number={0.claim_number!r}".format(self)


class Submission(models.Model):
    raw_xml = models.TextField()

    created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('-created',)
        get_latest_by = 'created'

    def __str__(self):
        return "pk={0.pk} raw_xml={0.raw_xml!r}".format(self)


class BCDS1MessageSubmission(models.Model):
    bcds1_message = models.OneToOneField(
        BCDS1Message,
        unique=True,
        on_delete=models.CASCADE,
        related_name='submission',
    )

    submission = models.ForeignKey(
        Submission,
        on_delete=models.CASCADE,
        related_name='bcds1_message_submissions',
    )

    state = models.IntegerField(choices=(
        (0, "Sent"),
        (1, "Success"),
        (2, "Failure"),
    ))

    response = models.TextField()

    ordering = models.IntegerField()

    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('ordering',)
        get_latest_by = 'created'
        unique_together = (
            ('submission', 'ordering'),
        )

    def __str__(self):
        return "submission_id={0.submission_id} " \
            "bcds1_message_id={0.bcds1_message_id!r}".format(self)
