import datetime
from unittest import mock
from opal.core.test import OpalTestCase
from odonto.episode_categories import (
    FP17OEpisode,  FP17Episode
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
        self.current_date = datetime.date(2020, 1, 1)
        self.previous_date = datetime.date(2019, 1, 1)

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
            "performer_info": {}
        }

    @mock.patch('odonto.views.Stats.get_current_financial_year')
    def test_single_current_fp17_episode(self, current_financial_year):
        current_financial_year.return_value = self.current_financial_year
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
        result = Stats().get_uda_data()


        result = Stats().get_context_data()
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
            "Band 1": 1,
            "Band 2": 0,
            "Band 3": 0,
            "uoa": 0
        }]
        result = Stats().get_context_data()
        self.assertEqual(result, expected)

    @mock.patch('odonto.views.Stats.get_current_financial_year')
    def test_single_current_fp17o_episode(self, current_financial_year):
        current_financial_year.return_value = self.current_financial_year
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
        result = Stats().get_uda_data()


        result = Stats().get_context_data()
        expected = self.expected()
        expected["state_counts"]["fp17os"]["total"] = 1
        expected["state_counts"]["fp17os"]["submitted"] = 1
        expected["month_totals"]["current"][9] = 1
        expected["uoa_info"]["by_period"]["current"][9] = 1
        expected["uoa_info"]["total"] = 1
        expected["performer_info"] = [{
            "name": "Jane Doe",
            "uda": 0,
            "Band 1": 0,
            "Band 2": 0,
            "Band 3": 0,
            "uoa": 1
        }]
        result = Stats().get_context_data()
        self.assertEqual(result, expected)
