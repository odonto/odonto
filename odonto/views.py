"""
Odonto views
"""
import datetime
import json
import csv
from collections import defaultdict, OrderedDict
from dateutil.relativedelta import relativedelta
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, DetailView, View, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseBadRequest
from odonto import episode_categories
from odonto import models
from odonto.utils import get_current_financial_year
from opal.models import Episode


def has_open_fp17(patient):
    return patient.episode_set.filter(
        category_name='FP17').exclude(stage__in=[
            episode_categories.FP17Episode.NEW,
            episode_categories.FP17Episode.SUBMITTED
        ]).exists()


def has_open_fp17o(patient):
    return patient.episode_set.filter(
        category_name='FP17O').exclude(stage__in=[
            episode_categories.FP17Episode.NEW,
            episode_categories.FP17Episode.SUBMITTED
        ]).exists()


class OpenFP17s(TemplateView):
    template_name = "open_list.html"

    def get_fp17s(self):
        qs = Episode.objects.filter(stage="Open")
        qs = episode_categories.get_episodes_for_user(
            qs, self.request.user
        )

        unsubmitted = episode_categories.get_unsubmitted_compass_episodes(qs)
        unsubmitted_ids = unsubmitted.values_list("id", flat=True)
        return qs.exclude(id__in=unsubmitted_ids)


class AllUnsubmitted(LoginRequiredMixin, TemplateView):
    template_name = "all_unsubmitted_list.html"

    def get_fp17s(self):
        qs = Episode.objects.all()
        result = episode_categories.get_unsubmitted_compass_episodes(qs)
        return sorted(
            result,
            key=lambda x: x.category.get_sign_off_date() or datetime.date.min
        )


class UnsubmittedFP17s(LoginRequiredMixin, TemplateView):
    template_name = "unsubmitted_list.html"

    def get_fp17s(self):
        qs = Episode.objects.all()
        qs = episode_categories.get_episodes_for_user(
            qs, self.request.user
        )
        return episode_categories.get_unsubmitted_compass_episodes_for_user(
            self.request.user
        )


class ViewFP17DetailView(LoginRequiredMixin, DetailView):
    model = Episode
    template_name = 'view_fp17.html'


class ViewFP17ODetailView(LoginRequiredMixin, DetailView):
    model = Episode
    template_name = 'view_fp17_o.html'


class CaseMix(LoginRequiredMixin, View):
    # only look patients after the rollout
    CASE_MIX_ROLLOUT = datetime.date(2020, 11, 1)

    def get_qs(self):
        return Episode.objects.filter(
            category_name__in=[
                episode_categories.FP17Episode.display_name,
                episode_categories.FP17OEpisode.display_name
            ]
        ).filter(
            stage=episode_categories.AbstractOdontoCategory.SUBMITTED
        ).prefetch_related(
            "orthodonticassessment_set",
            "orthodontictreatment_set",
            "fp17incompletetreatment_set",
            "casemix_set",
        )

    def get_empty_row(self):
        headers = ["Period start", "Year", "Month", "Total patients"]
        headers.extend(list(models.CaseMix.CASE_MIX_FIELDS.keys()))
        headers.extend([
            "Total score",
            models.CaseMix.STANDARD_PATIENT,
            models.CaseMix.SOME_COMPLEXITY,
            models.CaseMix.MODERATE_COMPLEXITY,
            models.CaseMix.SEVERE_COMPLEXITY,
            models.CaseMix.EXTREME_COMPLEXITY,

        ])
        return OrderedDict([(self.get_field_title(i), 0) for i in headers])

    def get_field_title(self, field_name):
        return field_name.replace("_", " ").capitalize()

    def calculate(self, qs):
        """
        returns a dictionary of dictionaries keyed by a month_year tuple
        i.e.
        {
            {{ sign_off_month_year_tuple }}: {
                ability_to_communicate: {{ sum of all ability_to_communicate for month_year}},
                ...
            }
        }
        """
        result = defaultdict(self.get_empty_row)

        for episode in qs:
            d = episode.category.get_sign_off_date()
            if not d or d <= self.CASE_MIX_ROLLOUT:
                continue
            d = (d.month, d.year)
            case_mix = episode.casemix_set.all()[0]
            result[d]["Total patients"] += 1
            for field in case_mix.CASE_MIX_FIELDS.keys():
                score = case_mix.score(field)
                if score is not None:
                    result[d][self.get_field_title(field)] += score
            total_score = case_mix.total_score()
            if total_score is not None:
                result[d]["Total score"] += total_score
            band = case_mix.band()
            result[d][band] += 1
        return result

    def get_period_start(self, month_year):
        """
        takes in a month_year e.g. 4, 2020
        and returns it as a string ie 202004
        """
        month, year = month_year
        return int("{}{}".format(year, str(month).zfill(2)))

    def create_response(self, date_to_values):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="case_mix.csv"'
        ordering = sorted(
            list(date_to_values.keys()),
            key=self.get_period_start,
            reverse=True
        )
        fieldnames = list(self.get_empty_row().keys())

        writer = csv.DictWriter(response, fieldnames=fieldnames)
        writer.writeheader()

        for month_year in ordering:
            row = {}
            val_dict = date_to_values[month_year]
            for key, val in val_dict.items():
                row[self.get_field_title(key)] = val
            row["Period start"] = self.get_period_start(month_year)
            row["Month"] = month_year[0]
            row["Year"] = month_year[1]
            writer.writerow(row)
        return response

    def get(self, *args, **kwargs):
        qs = self.get_qs()
        date_to_values = self.calculate(qs)
        return self.create_response(date_to_values)


class Stats(LoginRequiredMixin, TemplateView):
    template_name = "stats.html"

    def get_previous_financial_year(self):
        current_start = get_current_financial_year()[0]
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
        ).values_list('id', flat=True)
        assessment = Episode.objects.filter(
            category_name=episode_categories.FP17OEpisode.display_name
        ).filter(
            orthodontictreatment__completion_type=None
        ).filter(
            orthodonticassessment__date_of_assessment__range=date_range
        ).values_list('id', flat=True)
        episode_ids = set(list(completed) + list(assessment))
        return Episode.objects.filter(id__in=episode_ids)

    def get_successful_fp17os(self, date_range):
        return episode_categories.FP17OEpisode.get_successful_episodes(
            self.get_fp17o_qs(date_range)
        )

    def month_iterator(self, start_date):
        for i in range(0, 12):
            date_range = (
                start_date + relativedelta(months=i),
                start_date + relativedelta(months=i+1) - datetime.timedelta(1)
            )
            yield date_range

    def get_month_totals(self):
        result = {}
        monthly_claims = []
        time_periods = {
            "current": get_current_financial_year(),
            "previous": self.get_previous_financial_year()
        }
        for period_name, period_range in time_periods.items():
            monthly_claims = []
            for date_range in self.month_iterator(period_range[0]):
                successful_fp17o_count = self.get_successful_fp17os(date_range).count()
                successful_fp17_count = self.get_successful_fp17s(date_range).count()
                monthly_claims.append(
                    successful_fp17o_count + successful_fp17_count
                )
            result[period_name] = monthly_claims
        return result

    def get_state_counts(self):
        current_financial_year = get_current_financial_year()
        return {
            "fp17s": {
                "total": self.get_fp17_qs(current_financial_year).count(),
                "submitted": self.get_successful_fp17s(current_financial_year).count(),
                "open": self.get_fp17_qs(current_financial_year).filter(
                    stage=episode_categories.FP17Episode.OPEN
                ).count()
            },
            "fp17os": {
                "total": self.get_fp17o_qs(current_financial_year).count(),
                "submitted": self.get_successful_fp17os(current_financial_year).count(),
                "open": self.get_fp17o_qs(current_financial_year).filter(
                    stage=episode_categories.FP17OEpisode.OPEN
                ).count()
            }
        }

    def get_uoa_data(self):
        current_financial_year = get_current_financial_year()
        time_periods = {
            "current": get_current_financial_year(),
            "previous": self.get_previous_financial_year()
        }
        by_period = defaultdict(list)
        by_performer = defaultdict(int)

        for period_name, period_range in time_periods.items():
            for date_range in self.month_iterator(period_range[0]):
                fp17os = self.get_successful_fp17os(date_range)
                fp17os = fp17os.prefetch_related(
                    'orthodonticassessment_set',
                    'orthodontictreatment_set',
                    'fp17dentalcareprovider_set',
                )
                month_uoa_total = 0
                for fp17o in fp17os:
                    uoa = fp17o.category.uoa()
                    if not uoa:
                        continue

                    month_uoa_total += uoa
                    if period_name == "current":
                        performer = fp17o.fp17dentalcareprovider_set.all()[0].performer
                        by_performer[performer] += uoa
                by_period[period_name].append(month_uoa_total)
        return by_period, by_performer

    def get_uda_data(self):
        current_financial_year = get_current_financial_year()
        time_periods = {
            "current": get_current_financial_year(),
            "previous": self.get_previous_financial_year()
        }
        by_period = defaultdict(list)
        by_performer = defaultdict(lambda: defaultdict(int))

        for period_name, period_range in time_periods.items():
            for date_range in self.month_iterator(period_range[0]):
                fp17s = self.get_successful_fp17s(date_range)
                fp17s = fp17s.prefetch_related(
                    'fp17treatmentcategory_set',
                    'fp17dentalcareprovider_set'
                )
                month_uda_total = 0
                for fp17 in fp17s:
                    uda = fp17.category.uda()
                    if not uda:
                        continue

                    month_uda_total += uda
                    if period_name == "current":
                        treatment = fp17.fp17treatmentcategory_set.all()[0]
                        performer = fp17.fp17dentalcareprovider_set.all()[0].performer
                        by_performer[performer]["uda"] += uda
                        by_performer[performer][treatment.treatment_category] += 1
                by_period[period_name].append(round(month_uda_total))
        return by_period, by_performer

    def aggregate_performer_information(self, uda_by_performer, uoa_by_performer):
        result = []
        uda_performers = list(uda_by_performer.keys())
        uoa_performers = list(uoa_by_performer.keys())
        performers = list(set(uda_performers + uoa_performers))
        performers = sorted(performers)
        fp17s = self.get_successful_fp17s(
            get_current_financial_year()
        )

        for performer in performers:
            row = {"name": performer}
            fp17_performer = uda_by_performer.get(performer, {})
            row["uda"] = round(fp17_performer.get("uda", 0))
            row["band_1"] = fp17_performer.get(
                models.Fp17TreatmentCategory.BAND_1, 0
            )
            row["band_2"] = fp17_performer.get(
                models.Fp17TreatmentCategory.BAND_2, 0
            )
            row["band_3"] = fp17_performer.get(
                models.Fp17TreatmentCategory.BAND_3, 0
            )
            row["uoa"] = uoa_by_performer.get(performer, 0)
            result.append(row)
        return result

    def get_context_data(self):
        current_financial_year = get_current_financial_year()
        previous_financial_year = self.get_previous_financial_year()
        uda_by_period, uda_by_performer = self.get_uda_data()
        uoa_by_period, uoa_by_performer = self.get_uoa_data()
        performer_info = self.aggregate_performer_information(
            uda_by_performer, uoa_by_performer
        )
        current = "{}-{}".format(
            current_financial_year[0].year,
            current_financial_year[0].year + 1,
        )
        previous = "{}-{}".format(
            previous_financial_year[0].year,
            previous_financial_year[0].year + 1,
        )
        return {
            "current": current,
            "previous": previous,
            "state_counts": self.get_state_counts(),
            "month_totals": json.dumps(self.get_month_totals()),
            "uda_info": {
                "total":  sum(uda_by_period["current"]),
                "by_period": json.dumps(uda_by_period)
            },
            "uoa_info": {
                "total":  sum(uoa_by_period["current"]),
                "by_period": json.dumps(uoa_by_period)
            },
            "performer_info": performer_info
        }


class DeleteEpisode(LoginRequiredMixin, RedirectView):
    """
    This view is for when an episode has been opened in error
    it deletes and redirects to the patient detail page.

    Note the way Odonto functions is that a patient
    always has a new episode. So after it has deleted
    it creates an episode of the same category with
    the stage of new if it does not already exist
    """
    def get_redirect_url(self, *args, **kwargs):
        return f'/#/patient/{self.kwargs["patient_pk"]}'

    def post(self, *args, **kwargs):
        episode = get_object_or_404(Episode, pk=kwargs["episode_pk"])
        patient = episode.patient
        category_name = episode.category_name
        if category_name == episode_categories.DentalCareEpisodeCategory.display_name:
            return HttpResponseBadRequest()
        new = episode.category.NEW
        if episode.stage == episode.category.SUBMITTED:
            return HttpResponseBadRequest()
        episode.delete()
        patient.episode_set.get_or_create(
            category_name=category_name,
            stage=new
        )
        return super().post(*args, **kwargs)
