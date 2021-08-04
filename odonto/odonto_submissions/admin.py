import datetime
from django.contrib import admin
from opal import models as opal_models
from . import models
from reversion.admin import VersionAdmin
from odonto.episode_categories import FP17Episode, FP17OEpisode
from django.utils.html import format_html


SEND_ALL_AFTER_DATE = datetime.date(2020, 4, 1)


class SubmissionStateFilter(admin.SimpleListFilter):
    title = 'Submission state'
    parameter_name = 'submission_state'

    FP17_SUCCESS = "fp17_success"
    FP17_REJECTED = "fp17_rejected"
    FP17_NOT_SENT = "fp17_recent_not_sent"

    FP17O_SUCCESS = "fp17o_success"
    FP17O_REJECTED = "fp17o_rejected"
    FP17O_NOT_SENT = "fp17o_recent_not_sent"

    def lookups(self, request, model_admin):
        return (
            (self.FP17_SUCCESS, 'FP17 success',),
            (self.FP17_REJECTED, 'FP17 rejected',),
            (self.FP17_NOT_SENT, 'FP17 not sent',),
            (self.FP17O_SUCCESS, 'FP17O success',),
            (self.FP17O_REJECTED, 'FP17O rejected',),
            (self.FP17O_NOT_SENT, 'FP17O Not sent',),
        )

    def queryset(self, request, queryset):
        v = self.value()
        if not v:
            return queryset

        if v.startswith("fp17_"):
            queryset = queryset.filter(
                category_name=FP17Episode.display_name
            )
            if v == self.FP17_SUCCESS:
                return FP17Episode.get_successful_episodes(queryset)
            elif v == self.FP17_REJECTED:
                return FP17Episode.get_rejected_episodes(queryset)
            elif v == self.FP17_NOT_SENT:
                return queryset.filter(stage=FP17Episode.SUBMITTED).filter(
                    submission=None
                )
        elif v.startswith("fp17o_"):
            queryset = queryset.filter(
                category_name=FP17OEpisode.display_name
            )
            if v == self.FP17O_SUCCESS:
                return FP17OEpisode.get_successful_episodes(queryset)
            elif v == self.FP17O_REJECTED:
                return FP17OEpisode.get_rejected_episodes(queryset)
            elif v == self.FP17O_NOT_SENT:
                return queryset.filter(stage=FP17OEpisode.SUBMITTED).filter(
                    submission=None
                )
        return queryset


class SubmissionTimeFilter(admin.SimpleListFilter):
    title = 'Submission time'
    parameter_name = 'submission_time'

    def lookups(self, request, model_admin):
        return (
            ('recent', 'Recently submitted',),
        )

    def queryset(self, request, queryset):
        fp17_and_fp17os = [FP17Episode.display_name, FP17OEpisode.display_name]
        queryset = queryset.filter(category_name__in=fp17_and_fp17os)
        if self.value() == 'recent':
            queryset = queryset.prefetch_related('fp17incompletetreatment_set')
            queryset = queryset.prefetch_related('orthodonticassessment_set')
            queryset = queryset.prefetch_related('orthodontictreatment_set')
            ids = []
            for i in queryset:
                sign_off = i.category.get_sign_off_date()
                if sign_off and sign_off >= SEND_ALL_AFTER_DATE:
                    ids.append(i.id)
            return queryset.filter(id__in=ids)
        return queryset


class EpisodeAdmin(VersionAdmin):
    list_display = (
        'id', 'category_name', 'edit_form', 'submission_form', 'state', 'rejection',
    )
    list_filter = (SubmissionTimeFilter, SubmissionStateFilter,)

    actions = ["submit_episode_to_compass", "ignore_episode"]

    def submit_episode_to_compass(self, request, queryset):
        for episode in queryset:
            models.Submission.send(episode)

    submit_episode_to_compass.short_description = "Submit episode to compass"

    def ignore_episode(self, request, queryset):
        for episode in queryset:
            if episode.category_name not in [
                FP17Episode.display_name, FP17OEpisode.display_name
            ]:
                continue
            submission = episode.category.submission()
            if submission and submission.state == submission.REJECTED_BY_COMPASS:
                episode.episodesbeinginvestigated_set.create()

    ignore_episode.short_description = "Ignore this episode's rejection"

    def submission_form(self, obj):
        if obj.category_name not in [
            FP17Episode.display_name, FP17OEpisode.display_name
        ]:
            return ""
        if obj.category_name == FP17Episode.display_name:
            url = "/pathway/#/fp17-submit/{}/{}"
        elif obj.category_name == FP17OEpisode.display_name:
            url = "/pathway/#/fp17-o-submit/{}/{}"
        else:
            return ""

        url = url.format(obj.patient_id, obj.id)
        return format_html('<a href="{}">{}</a>', url, url)

    def edit_form(self, obj):
        if obj.category_name not in [
            FP17Episode.display_name, FP17OEpisode.display_name
        ]:
            return ""
        if obj.category_name == FP17Episode.display_name:
            url = "/pathway/#/fp17-edit/{}/{}"
        elif obj.category_name == FP17OEpisode.display_name:
            url = "/pathway/#/fp17-o-edit/{}/{}"
        else:
            return ""

        url = url.format(obj.patient_id, obj.id)
        return format_html('<a href="{}">{}</a>', url, url)

    def state(self, obj):
        if obj.category_name not in [
            FP17Episode.display_name, FP17OEpisode.display_name
        ]:
            return ""
        submission = obj.category.submission()
        if not submission:
            return obj.stage
        if submission.state == submission.REJECTED_BY_COMPASS:
            if obj.episodesbeinginvestigated_set.exists():
                return "Rejected but ignored"
        return submission.state

    def rejection(self, obj):
        submission = obj.category.submission()
        if submission:
            return submission.rejection
        return ""

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.prefetch_related('submission_set')
        return qs


class SubmissionAdmin(VersionAdmin):
    list_display = ('id', 'episode_id', 'first_name', 'surname', 'created', 'state',)
    list_editable = ("state",)
    list_filter = ('state',)
    ordering = ('-created',)

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
