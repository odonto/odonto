from django.contrib import admin
from opal import models as opal_models
from . import models
from reversion.admin import VersionAdmin
from odonto import episode_categories
import dateutil.relativedelta


class EpisodeAdmin(VersionAdmin):
    list_display = (
        'id', 'category_name', 'stage', 'submission_deadline',
        'last_submission_state', 'last_submission_created'
    )

    def submission_deadline(self, obj):
        fp17_name = episode_categories.FP17Episode.display_name
        if not obj.category_name == fp17_name:
            return "NA"
        fp17_incomplete_treatment = obj.fp17incompletetreatment_set.all()[0]
        last_visit = fp17_incomplete_treatment.completion_or_last_visit
        if last_visit:
            return last_visit - dateutil.relativedelta.relativedelta(months=3)

    def last_submission_state(self, obj):
        fp17_name = episode_categories.FP17Episode.display_name
        if not obj.category_name == fp17_name:
            return "NA"
        if obj.submission_set.all():
            submission = list(obj.submission_set.all())[-1]
            return submission.state

    def last_submission_created(self, obj):
        if obj.submission_set.all():
            submission = list(obj.submission_set.all())[-1]
            return submission.submission_dt

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.prefetch_related('submission_set')
        qs = qs.prefetch_related('fp17incompletetreatment_set')
        return qs


admin.site.unregister(opal_models.Episode)
admin.site.register(opal_models.Episode, EpisodeAdmin)

admin.site.register(models.CompassBatchResponse)
admin.site.register(models.Submission)
admin.site.register(models.SystemClaim)
