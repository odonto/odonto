from django.contrib import admin
from opal import models as opal_models
from . import models
from reversion.admin import VersionAdmin
from odonto import episode_categories
from django.utils.html import format_html


class EpisodeAdmin(VersionAdmin):
    list_display = (
        'id', 'category_name', 'stage',
        'submission_state', 'summary'
    )

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

    def submission_state(self, obj):
        if obj.category.display_name == episode_categories.DentalCareEpisodeCategory.display_name:
            return
        submission = obj.category.submission()
        if submission:
            return submission.state

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.prefetch_related('submission_set')
        return qs


class SubmissionAdmin(VersionAdmin):
    list_display = ('id', 'episode_id', 'first_name', 'surname', 'created', 'state',)
    list_editable = ("state",)
    list_filter = ('state',)

    def first_name(self, obj):
        return obj.episode.patient.demographics().first_name

    def surname(self, obj):
        return obj.episode.patient.demographics().surname


admin.site.unregister(opal_models.Episode)
admin.site.register(opal_models.Episode, EpisodeAdmin)

admin.site.register(models.Response)
admin.site.register(models.Submission, SubmissionAdmin)
admin.site.register(models.Transmission)
admin.site.register(models.EpisodesBeingInvestigated)
