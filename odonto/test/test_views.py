import datetime
import json
import csv
from unittest import mock
from django.urls import reverse
from opal.core.test import OpalTestCase
from odonto.episode_categories import (
    FP17OEpisode,  FP17Episode, DentalCareEpisodeCategory
)
from odonto.models import Fp17TreatmentCategory, OrthodonticAssessment
from odonto.odonto_submissions.models import Submission
from odonto.views import Stats


class GetContextDataStatsTestCase(OpalTestCase):
    def setUp(self):
        self.current_financial_year = (
            datetime.date(2019, 4, 1),
            datetime.date(2020, 3, 31),
        )
        self.previous_financial_year = (
            datetime.date(2018, 4, 1),
            datetime.date(2019, 3, 31),
        )
        self.current_date = datetime.date(2020, 1, 1)
        self.previous_date = datetime.date(2019, 1, 1)
        self.view = Stats()

    def new_fp17_episode(self):
        patient, episode = self.new_patient_and_episode_please()
        episode.category_name = FP17Episode.display_name
        episode.save()
        episode.fp17dentalcareprovider_set.update(
            performer="Jane Doe"
        )
        patient.demographics_set.update(
            date_of_birth=datetime.date(1991, 2, 2)
        )
        return episode

    def new_fp17o_episode(self):
        patient, episode = self.new_patient_and_episode_please()
        episode.category_name = FP17OEpisode.display_name
        episode.save()
        episode.fp17dentalcareprovider_set.update(
            performer="Jane Doe"
        )
        patient.demographics_set.update(
            date_of_birth=datetime.date(1991, 2, 2)
        )
        return episode

    def expected(self):
        return {
            'menu_years': [2019, 2020, 2021, 2022],
            'current': '2019-2020',
            'previous': '2018-2019',
            "state_counts": {
                "fp17s": {
                    "total": 0,
                    "submitted": 0,
                    "open": 0,
                },
                "fp17os": {
                    "total": 0,
                    "submitted": 0,
                    "open": 0,
                }
            },
            "month_totals": {
                "current": [0 for i in range(12)],
                "previous": [0 for i in range(12)],
            },
            "uda_info": {
                "by_period": {
                    "current": [0 for i in range(12)],
                    "previous": [0 for i in range(12)],
                },
                "total": 0,
            },
            "uoa_info": {
                "by_period": {
                    "current": [0 for i in range(12)],
                    "previous": [0 for i in range(12)],
                },
                "total": 0,
            },
            "performer_info": {},
            "view": self.view
        }

    @mock.patch('odonto.views.Stats.date_range')
    @mock.patch('odonto.views.Stats.previous_date_range')
    def test_single_current_fp17_episode(self, previous_date_range, date_range):
        self.maxDiff = None
        date_range.__get__ = mock.Mock(return_value=self.current_financial_year)
        previous_date_range.__get__ = mock.Mock(return_value=self.previous_financial_year)
        episode = self.new_fp17_episode()
        episode.stage = FP17Episode.SUBMITTED
        episode.save()
        episode.fp17incompletetreatment_set.update(
            completion_or_last_visit=self.current_date
        )
        episode.fp17treatmentcategory_set.update(
            treatment_category=Fp17TreatmentCategory.BAND_1
        )
        episode.submission_set.create(
            state=Submission.SUCCESS
        )
        result = self.view.get_context_data()
        expected = self.expected()
        expected["state_counts"]["fp17s"]["total"] = 1
        expected["state_counts"]["fp17s"]["submitted"] = 1
        expected["month_totals"]["current"][9] = 1
        expected["uda_info"]["by_period"]["current"][9] = 1
        expected["uda_info"]["total"] = 1
        expected["uoa_info"]["total"] = 0
        expected["performer_info"] = [{
            "name": "Jane Doe",
            "uda": 1,
            "band_1": 1,
            "band_2": 0,
            "band_3": 0,
            "uoa": 0
        }]
        expected["month_totals"] = json.dumps(
            expected["month_totals"]
        )
        expected["uda_info"]["by_period"] = json.dumps(
            expected["uda_info"]["by_period"]
        )
        expected["uoa_info"]["by_period"] = json.dumps(
            expected["uoa_info"]["by_period"]
        )
        result = self.view.get_context_data()
        self.assertEqual(result, expected)

    @mock.patch('odonto.views.Stats.date_range')
    @mock.patch('odonto.views.Stats.previous_date_range')
    def test_single_current_fp17o_episode(self, previous_date_range, date_range):
        date_range.__get__ = mock.Mock(return_value=self.current_financial_year)
        previous_date_range.__get__ = mock.Mock(return_value=self.previous_financial_year)
        episode = self.new_fp17o_episode()
        episode.stage = FP17Episode.SUBMITTED
        episode.save()
        episode.orthodonticassessment_set.update(
            date_of_assessment=self.current_date,
            assessment=OrthodonticAssessment.ASSESSMENT_AND_REVIEW
        )
        episode.patient.demographics_set.update(
            date_of_birth=datetime.date(2000, 1, 1)
        )
        episode.fp17incompletetreatment_set.update(
            completion_or_last_visit=self.current_date
        )
        episode.fp17treatmentcategory_set.update(
            treatment_category=Fp17TreatmentCategory.BAND_1
        )
        episode.submission_set.create(
            state=Submission.SUCCESS
        )

        expected = self.expected()
        expected["state_counts"]["fp17os"]["total"] = 1
        expected["state_counts"]["fp17os"]["submitted"] = 1
        expected["month_totals"]["current"][9] = 1
        expected["uoa_info"]["by_period"]["current"][9] = 1
        expected["uoa_info"]["total"] = 1
        expected["performer_info"] = [{
            "name": "Jane Doe",
            "uda": 0,
            "band_1": 0,
            "band_2": 0,
            "band_3": 0,
            "uoa": 1
        }]
        expected["month_totals"] = json.dumps(
            expected["month_totals"]
        )
        expected["uda_info"]["by_period"] = json.dumps(
            expected["uda_info"]["by_period"]
        )
        expected["uoa_info"]["by_period"] = json.dumps(
            expected["uoa_info"]["by_period"]
        )
        result = self.view.get_context_data()
        self.assertEqual(result, expected)


class CaseMixTestCase(OpalTestCase):
    def setUp(self):
        self.url = reverse("case-mix-csv")
        # create the user
        self.user
        self.assertTrue(
            self.client.login(
                username=self.USERNAME,
                password=self.PASSWORD
            )
        )

    def test_none(self):
        response = self.client.get(self.url)
        self.assertEquals(
            response.get('Content-Disposition'),
            'attachment; filename="case_mix.csv"'
        )
        reader = list(csv.reader(response.content.decode("utf-8").strip().split("\n")))
        self.assertEqual(len(reader), 1)
        self.assertIn("Period start", reader[0])

    def test_old(self):
        _, self.episode = self.new_patient_and_episode_please()
        self.episode.category_name = FP17Episode.display_name
        self.episode.stage = FP17Episode.SUBMITTED
        self.episode.save()
        self.episode.fp17incompletetreatment_set.update(
            completion_or_last_visit=datetime.date(
                2020, 10, 28
            )
        )
        self.episode.casemix_set.update(
            ability_to_communicate="0",
            ability_to_cooperate="0",
            medical_status="A",
            oral_risk_factors="C",
            access_to_oral_care="0",
            legal_and_ethical_barriers_to_care="0"
        )
        response = self.client.get(self.url)
        self.assertEquals(
            response.get('Content-Disposition'),
            'attachment; filename="case_mix.csv"'
        )
        reader = list(csv.reader(response.content.decode("utf-8").strip().split("\n")))
        self.assertEqual(len(reader), 1)
        self.assertIn("Period start", reader[0])

    def test_vanilla(self):
        _, self.episode = self.new_patient_and_episode_please()
        self.episode.category_name = FP17Episode.display_name
        self.episode.stage = FP17Episode.SUBMITTED
        self.episode.save()
        self.episode.fp17incompletetreatment_set.update(
            completion_or_last_visit=datetime.date(
                2021, 8, 1
            )
        )
        self.episode.casemix_set.update(
            ability_to_communicate="0",
            ability_to_cooperate="0",
            medical_status="A",
            oral_risk_factors="C",
            access_to_oral_care="0",
            legal_and_ethical_barriers_to_care="0"
        )
        response = self.client.get(self.url)
        self.assertEquals(
            response.get('Content-Disposition'),
            'attachment; filename="case_mix.csv"'
        )
        reader = list(csv.DictReader(response.content.decode("utf-8").strip().split("\n")))
        self.assertEqual(len(reader), 1)
        expected = {
            "Period start": "202108",
            "Year": "2021",
            "Month": "8",
            'Ability to communicate': '0',
            'Ability to cooperate': '0',
            'Medical status': '2',
            'Oral risk factors': '12',
            'Access to oral care': '0',
            'Legal and ethical barriers to care': '0',
            'Total patients': '1',
            'Total score': '14',
            'Standard patient': '0',
            'Some complexity': '0',
            'Moderate complexity': '1',
            'Severe complexity': '0',
            'Extreme complexity': '0'
        }
        self.assertEqual(
            dict(reader[0]),
            expected
        )


class DeleteEpisodeTestCase(OpalTestCase):
    def setUp(self):
        self.patient, self.episode = self.new_patient_and_episode_please()
        # initialise the user property so we can log in
        self.user
        self.url = reverse("delete-episode", kwargs={
            "patient_pk": self.patient.pk,
            "episode_pk": self.episode.pk
        })
        self.assertTrue(
            self.client.login(
                username=self.user.username, password=self.PASSWORD
            )
        )
        self.assertTrue(
            self.client.login(
                username=self.user.username, password=self.PASSWORD
            )
        )

    def test_delete_and_redirect(self):
        self.episode.category_name = FP17Episode.display_name
        self.episode.stage = FP17Episode.OPEN
        self.episode.save()
        other_episode = self.patient.episode_set.create(
            category_name=FP17Episode.display_name,
            stage=FP17Episode.NEW
        )
        response = self.client.post(self.url)
        self.assertRedirects(response, f'/#/patient/{self.patient.id}')
        self.assertEqual(
            self.patient.episode_set.get().id, other_episode.id
        )

    def test_delete_create_new_stage_and_redirect(self):
        self.episode.category_name = FP17Episode.display_name
        self.episode.stage = FP17Episode.NEW
        self.episode.save()
        response = self.client.post(self.url)
        other_episode = self.patient.episode_set.get()
        self.assertRedirects(response, f'/#/patient/{self.patient.id}')
        self.assertEqual(
            other_episode.patient_id, self.patient.id
        )
        self.assertEqual(
            other_episode.category_name, FP17Episode.display_name
        )
        self.assertEqual(
            other_episode.stage, FP17Episode.NEW
        )

    def test_dental_care_episode(self):
        self.episode.category_name = DentalCareEpisodeCategory.display_name
        self.episode.save()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.patient.episode_set.get().id, self.episode.id)

    def test_episode_submitted(self):
        self.episode.stage = FP17Episode.SUBMITTED
        self.episode.save()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.patient.episode_set.get().id, self.episode.id)
