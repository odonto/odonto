import datetime
from django.contrib import admin
from opal import models as opal_models
from odonto import models as odonto_models
from . import models
from reversion.admin import VersionAdmin
from odonto import episode_categories
from dateutil.relativedelta import relativedelta
from django.utils.html import format_html


class OldestFP17(admin.SimpleListFilter):
    title = "Old FP17s"
    NEARLY_THREE_MONTHS = 'nearly_3_months'
    OVER_THREE_MONTHS = 'over_3_months'
    NEARLY_TWO_MONTHS = 'nearly_2_months'
    OVER_TWO_MONTHS = 'over_2_months'

    parameter_name = "deadline"

    def lookups(self, request, model_admin):
        return (
            (self.NEARLY_THREE_MONTHS, 'Nearly 3 months'),
            (self.OVER_THREE_MONTHS, 'Over 3 month'),
            (self.NEARLY_TWO_MONTHS, 'Nearly 2 months'),
            (self.OVER_TWO_MONTHS, 'Oever 2 months'),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        treatments = odonto_models.Fp17IncompleteTreatment.objects.filter(
            episode__stage="Submitted"
        )
        treatments = treatments.filter(
            episode__category_name=episode_categories.FP17Episode.display_name
        )
        treatments = treatments.exclude(completion_or_last_visit=None)
        three_mo = datetime.date.today() - relativedelta(
            months=3
        )
        two_mo = datetime.date.today() - relativedelta(
            months=2
        )
        if self.value() == self.OVER_THREE_MONTHS:
            treatments = treatments.filter(
                completion_or_last_visit__lte=three_mo
            )
            return queryset.filter(
                id__in=treatments.values_list('episode_id', flat=True)
            )
        if self.value() == self.NEARLY_THREE_MONTHS:
            treatments = treatments.exclude(
                completion_or_last_visit__lte=three_mo
            ).filter(
                completion_or_last_visit__lte=three_mo + datetime.timedelta(7)
            )
            return queryset.filter(
                id__in=treatments.values_list('episode_id', flat=True)
            )

        if self.value() == self.OVER_TWO_MONTHS:
            treatments = treatments.filter(
                completion_or_last_visit__lte=two_mo
            )
            return queryset.filter(
                id__in=treatments.values_list('episode_id', flat=True)
            )
        if self.value() == self.NEARLY_TWO_MONTHS:
            treatments = treatments.exclude(
                completion_or_last_visit__lte=two_mo
            ).filter(
                completion_or_last_visit__lte=two_mo + datetime.timedelta(7)
            )
            return queryset.filter(
                id__in=treatments.values_list('episode_id', flat=True)
            )


class EpisodeAdmin(VersionAdmin):
    list_display = (
        'id', 'category_name', 'stage', 'submission_deadline',
        'last_submission_state', 'last_submission_created',
        'summary'
    )

    list_filter = (OldestFP17,)

    actions = ["submit_episode_to_compass"]

    def submit_episode_to_compass(self, request, queryset):
        for episode in queryset:
            models.Submission.send(episode)

    submit_episode_to_compass.short_description = "Submit episode to compass"

    def summary(self, obj):
        fp17_name = episode_categories.FP17Episode.display_name
        if not obj.category_name == fp17_name:
            return
        return format_html(
            "<a href='/#/summary/fp17/{}/{}'>summary</a>",
            obj.patient_id, obj.id
        )

    def submission_deadline(self, obj):
        fp17_name = episode_categories.FP17Episode.display_name
        if not obj.category_name == fp17_name:
            return "NA"
        fp17_incomplete_treatment = obj.fp17incompletetreatment_set.all()[0]
        last_visit = fp17_incomplete_treatment.completion_or_last_visit
        if last_visit:
            return last_visit + relativedelta(months=2)

    def last_submission_state(self, obj):
        fp17_name = episode_categories.FP17Episode.display_name
        if not obj.category_name == fp17_name:
            return "NA"
        if obj.submission_set.all():
            submission = list(obj.submission_set.all())[0]
            return submission.state

    def last_submission_created(self, obj):
        if obj.submission_set.all():
            submission = list(obj.submission_set.all())[0]
            return submission.created

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.prefetch_related('submission_set')
        qs = qs.prefetch_related('fp17incompletetreatment_set')
        return qs


class SubmissionAdmin(VersionAdmin):
    list_display = ('id', 'episode_id', 'created', 'state',)
    list_editable = ("state",)
    list_filter = ('state',)


admin.site.unregister(opal_models.Episode)
admin.site.register(opal_models.Episode, EpisodeAdmin)

admin.site.register(models.CompassBatchResponse)
admin.site.register(models.Submission, SubmissionAdmin)
admin.site.register(models.Transmission)
