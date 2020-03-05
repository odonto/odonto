"""
Odonto views
"""
import datetime
from collections import defaultdict
from dateutil.relativedelta import relativedelta
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from odonto import episode_categories
from odonto import models

from opal.models import Episode, Patient


def has_open_fp17(patient):
    return patient.episode_set.filter(
        category_name='FP17').exclude(
            stage__in=['New', 'Submitted']).exists()


def has_open_fp17o(patient):
    return patient.episode_set.filter(
        category_name='FP17O').exclude(
            stage__in=['New', 'Submitted']).exists()


class OpenFP17s(TemplateView):
    template_name = "open_list.html"

    def get_fp17_qs(self):
        qs = Episode.objects.filter(stage="Open")
        qs = episode_categories.get_episodes_for_user(
            qs, self.request.user
        )

        unsubmitted = episode_categories.get_unsubmitted_fp17_and_fp17os(qs)
        unsubmitted_ids = unsubmitted.values_list("id", flat=True)
        return qs.exclude(id__in=unsubmitted_ids)


class UnsubmittedFP17s(LoginRequiredMixin, TemplateView):
    template_name = "unsubmitted_list.html"

    def get_fp17_qs(self):
        qs = Episode.objects.all()
        qs = episode_categories.get_episodes_for_user(
            qs, self.request.user
        )
        return episode_categories.get_unsubmitted_fp17_and_fp17os_for_user(
            self.request.user
        )


class PatientDetailView(LoginRequiredMixin, DetailView):
    model = Patient

    def get_context_data(self, **k):
        """
        Add additional context variables to the patient
        detail view.
        """
        context = super().get_context_data(**k)
        patient = self.get_object()
        episodes = patient.episode_set.filter(category_name__in=['FP17', 'FP17O'])

        context['episodes']   = episodes
        context['open_fp17']  = has_open_fp17(patient)
        context['open_fp17o'] = has_open_fp17o(patient)

        context['new_fp17_pk']  = patient.episode_set.get(category_name='FP17', stage='New').pk
        context['new_fp17o_pk'] = patient.episode_set.get(category_name='FP17O', stage='New').pk

        return context


class FP17SummaryDetailView(LoginRequiredMixin, DetailView):
    model = Episode
    template_name = 'fp17_summary.html'


class ViewFP17DetailView(LoginRequiredMixin, DetailView):
    model = Episode
    template_name = 'view_fp17.html'


class FP17OSummaryDetailView(LoginRequiredMixin, DetailView):
    model = Episode
    template_name = 'fp17_o_summary.html'


class ViewFP17ODetailView(LoginRequiredMixin, DetailView):
    model = Episode
    template_name = 'view_fp17_o.html'


class Stats(LoginRequiredMixin, TemplateView):
    def get_current_financial_year(self):
        today = datetime.date.today()
        if today.month > 3:
            return (
                datetime.date(today.year, 4, 1),
                today
            )
        return (
            datetime.date(today.year-1, 4, 1),
            today
        )

    def get_previous_financial_year(self):
        current_start = self.get_current_financial_year()[0]
        return (
            datetime.date(
                current_start.year-1, current_start.month, current_start.day
            ),
            current_start - datetime.timedelta(1)
        )

    def get_fp17_qs(self, date_range):
        return Episode.objects.filter(
            category_name=episode_categories.FP17Episode.display_name
        ).filter(
            fp17incompletetreatment__completion_or_last_visit__range=date_range
        )

    def get_successful_fp17s(self, date_range):
        return episode_categories.FP17Episode.get_successful_episodes(
            self.get_fp17_qs(date_range)
        )

    def get_fp17o_qs(self, date_range):
        completed = Episode.objects.filter(
            category_name=episode_categories.FP17OEpisode.display_name
        ).exclude(
            orthodontictreatment__completion_type=None
        ).filter(
            orthodontictreatment__date_of_completion__range=date_range
        )
        assessment = Episode.objects.filter(
            category_name=episode_categories.FP17OEpisode.category_name
        ).filter(
            orthodontictreatment__completion_type=None
        ).filter(
            orthodonticassessment__date_of_assessment__range=date_range
        )
        return completed.union(assessment)

    def get_successful_fp17os(self, date_range):
        return episode_categories.FP17OEpisode.get_successful_episodes(
            self.get_fp17o_qs(date_range)
        )

    def month_iterator(self, start_date):
        for i in range(0, 11):
            date_range = (
                start_date + relativedelta(months=i),
                start_date + relativedelta(months=i+1)
            )
            yield date_range

    def get_month_totals(self):
        result = {}
        monthly_claims = []
        time_periods = {
            "current": self.get_current_financial_year(),
            "previous": self.get_previous_financial_year()
        }
        for period_name, period_range in time_periods.items():
            for date_range in self.month_iterator(period_range[0]):
                successful_fp17o_count = self.get_successful_fp17os(date_range).count()
                successful_fp17_count = self.get_successful_fp17s(date_range).count()
                monthly_claims.append(
                    successful_fp17o_count + successful_fp17_count
                )
            result[period_name] = monthly_claims
        return result

    def get_state_counts(self):
        current_financial_year = self.get_current_financial_year()

        # fp17s
        current_fp17s = self.self.get_fp17_qs(current_financial_year)
        submitted_fp17s = episode_categories.FP17Episode.get_successful_episodes(
            current_fp17s
        )
        open_fp17s = current_fp17s.filter(
            state=episode_categories.FP17Episode.OPEN
        )

        # fp17Os
        current_fp17os = self.self.get_fp17os(current_financial_year)
        submitted_fp17os = episode_categories.FP17OEpisode.get_successful_episodes(
            current_fp17os
        )
        open_fp17os = current_fp17os.filter(
            state=episode_categories.FP17OEpisode.OPEN
        )

        monthly_claims = []
        start_date = current_financial_year[0]
        for date_range in self.month_iterator(start_date):
            month_fp17s = self.get_fp17_qs(date_range)
            successful_month_fp17s = episode_categories.FP17Episode.get_successful_episodes(
                month_fp17s
            )
            month_fp17os = self.get_fp17os(date_range)
            successful_month_fp17os = episode_categories.FP17OEpisode.get_successful_episodes(
                month_fp17os
            )
            monthly_claims.append(
                successful_month_fp17s.count() + successful_month_fp17os.count()
            )

        return {
            "fp17s": {
                "total": current_fp17s.count(),
                "submitted": submitted_fp17s.count(),
                "open": open_fp17s.count()
            },
            "fp17os": {
                "total": current_fp17os.count(),
                "submitted": submitted_fp17os.count(),
                "open": open_fp17os.count()
            }
        }

    def get_fp17o_data(self):
        current_financial_year = self.get_current_financial_year()
        time_periods = {
            "current": self.get_current_financial_year(),
            "previous": self.get_previous_financial_year()
        }
        result = {}
        result["summary"] =  defaultdict(int)
        result["by_performer"] = defaultdict(int)

        for period_name, period_range in time_periods.items():
            for date_range in self.month_iterator(period_range[0]):
                fp17os = self.get_successful_fp17os(date_range)
                fp17os.prefetch_related(
                    'orthodonticassessment_set',
                    'orthodontictreatment_set',
                    'fp17dentalcareprovider_set'
                )
                month_uoa_total = 0
                for fp17o in fp17os:
                    uoa = fp17o.uoa()
                    month_uoa_total += uoa
                    if period_name == "current":
                        performer = fp17o.fp17dentalcareprovider_set.all()[0].performer
                        result["by_performer"][performer] += uoa
                result["summary"][period_name].append(month_uoa_total)
        result["summary"]["total"] = sum(result["current"].values())
        return result

    def get_fp17_data(self):
        current_financial_year = self.get_current_financial_year()
        time_periods = {
            "current": self.get_current_financial_year(),
            "previous": self.get_previous_financial_year()
        }
        result = {}
        result["summary"] = {}
        result["summary"]["by_period"] = defaultdict(list)
        result["summary"]["total"] = 0
        result["by_performer"] = defaultdict(lambda : defaultdict(int))

        for period_name, period_range in time_periods.items():
            for date_range in self.month_iterator(period_range[0]):
                fp17s = self.get_successful_fp17s(date_range)
                fp17s.prefetch_related(
                    'fp17treatmentcategory_set',
                    'fp17dentalcareprovider_set'
                )
                month_uoa_count = 0
                for fp17 in fp17s:
                    uda = fp17.uda()
                    month_uda_total += uda
                    result["summary"]["by_period"][period_name].append(month_uda_total)
                    if period_name == "current":
                        treatment = fp17.fp17treatmentcategory_set.all()[0]
                        performer = fp17o.fp17dentalcareprovider_set.all()[0].performer
                        result["by_performer"][performer]["uda"] += uoa
                        result["by_performer"][performer][treatment.treatment_category] += 1
                result["summary"][period_name].append(month_uda_total)
        result["summary"]["total"] = sum(result["current"].values())
        return result

    def aggregate_performer_information(self, fp17_info, fp17o_info):
        result = []
        uda_performers = fp17_info["by_perfomer"].keys()
        uoa_performers = fp17o_info["by_performer"].keys()
        performers = list(set(uda_performers + uoa_performers))
        performers = sorted(performers)
        fp17s = self.get_successful_fp17s(
            self.get_current_financial_year()
        )

        for performer in performers:
            row = {"name": performer}
            fp17_performance = uoa_data["by_performer"].get(performer, {})
            row["uda"] = fp17_performance.get("uda")
            row["Band 1"] = fp17_performance.get(
                models.Fp17TreatmentCategory.BAND_1, 0
            )
            row["Band 2"] = fp17_performance.get(
                models.Fp17TreatmentCategory.BAND_2, 0
            )
            row["Band 3"] = fp17_performance.get(
                models.Fp17TreatmentCategory.BAND_3, 0
            )
            row["uoa"] = uoa_data["by_performer"].get(performer, 0)
            result.append(row)

    def get_context_data(self):
        fp17_info = self.get_fp17_data()
        fp17o_info = self.get_fp17o_data()
        perfomer_info = self.aggregate_performer_information()
        return {
            "state_counts": self.get_state_counts(),
            "month_totals": self.get_month_totals(),
            "fp17_info": fp17_info["summary"],
            "fp17o_info": fp17o_info["summary"],
            "perfomer_info": performer_info
        }
