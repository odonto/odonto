"""
Unittests for odonto.pathways
"""
import datetime
from django.urls import reverse
from opal.models import Episode
from opal.core.test import OpalTestCase
from odonto import models
from odonto import episode_categories
from odonto import pathways
from odonto.odonto_submissions import models as submission_models

class GetSubmissionStateTestCase(OpalTestCase):
    def setUp(self):
        _, self.episode = self.new_patient_and_episode_please()

    def test_is_submitted_success(self):
        self.episode.submission_set.create(
            state=submission_models.Submission.SUCCESS
        )
        self.assertTrue(pathways.is_submitted(self.episode))

    def test_is_submitted_failed(self):
        self.episode.submission_set.create(
            state=submission_models.Submission.FAILED_TO_SEND
        )
        self.assertFalse(pathways.is_submitted(self.episode))

    def test_is_submitted_none(self):
        self.assertFalse(pathways.is_submitted(self.episode))

class AddPatientPathwayTestCase(OpalTestCase):
    def test_save(self):
        patient, episode = self.new_patient_and_episode_please()
        pathway = pathways.AddPatientPathway()
        pathway.save({}, patient=patient, episode=episode)
        self.assertEqual(1, patient.episode_set.filter(category_name="FP17").count())
        self.assertEqual(1, patient.episode_set.filter(category_name="FP17O").count())


class Fp17PathwayTestCase(OpalTestCase):

    def test_link(self):
        result = pathways.Fp17Pathway.get_absolute_url(
            ngepisode=2, ngpatient=1
        )
        self.assertEqual(
            result, "/pathway/#/fp17/[[ 1 ]]/[[ 2 ]]/"
        )


    def test_save_sets_stage(self):
        patient, episode = self.new_patient_and_episode_please()
        pathway = pathways.Fp17Pathway()
        fp17 = patient.create_episode(category_name='FP17', stage='New')
        pathway.save({}, patient=patient, episode=fp17)
        fp17 = Episode.objects.get(pk=fp17.pk)
        self.assertEqual('Open', fp17.stage)


class SubmitFP17PathwayTestCase(OpalTestCase):
    def setUp(self):
        self.patient, self.episode = self.new_patient_and_episode_please()
        self.other_episode = self.patient.create_episode()
        self.other_episode.category_name = episode_categories.FP17Episode.display_name
        self.other_episode.stage = episode_categories.FP17Episode.SUBMITTED
        self.other_episode.save()

        self.date_1 = datetime.date(2019, 10, 4)
        self.date_2 = datetime.date(2019, 10, 5)
        self.date_3 = datetime.date(2019, 10, 6)
        self.assertTrue(
            self.client.login(
                username=self.user.username, password=self.PASSWORD
            )
        )
        self.url = reverse(
            "pathway", kwargs=dict(
                name="fp17-submit",
                patient_id=self.patient.id,
                episode_id=self.episode.id
            )
        )
        self.pathway = pathways.SubmitFP17Pathway()

    def test_get_overlapping_dates_with_result(self):
        self.other_episode.fp17treatmentcategory_set.update(
            treatment_category=models.Fp17TreatmentCategory.BAND_1
        )
        self.other_episode.fp17incompletetreatment_set.update(
            date_of_acceptance=self.date_1,
            completion_or_last_visit=self.date_2
        )
        result = self.pathway.get_overlapping_dates(
            self.patient, self.episode
        )
        self.assertEqual(
            result, [(self.date_1, self.date_2,)]
        )

    def test_get_overlapping_dates_with_urgent_treatment(self):
        self.other_episode.fp17treatmentcategory_set.update(
            treatment_category=models.Fp17TreatmentCategory.URGENT_TREATMENT
        )
        self.other_episode.fp17incompletetreatment_set.update(
            date_of_acceptance=self.date_1,
            completion_or_last_visit=self.date_2
        )
        result = self.pathway.get_overlapping_dates(
            self.patient, self.episode
        )
        self.assertEqual(
            result, []
        )

    def test_get_overlapping_dates_with_no_date_of_acceptance(self):
        self.other_episode.fp17treatmentcategory_set.update(
            treatment_category=models.Fp17TreatmentCategory.BAND_1
        )
        self.other_episode.fp17incompletetreatment_set.update(
            completion_or_last_visit=self.date_2
        )
        result = self.pathway.get_overlapping_dates(
            self.patient, self.episode
        )
        self.assertEqual(
            result, []
        )

    def test_get_overlapping_dates_with_no_dates(self):
        self.other_episode.fp17treatmentcategory_set.update(
            treatment_category=models.Fp17TreatmentCategory.BAND_1
        )
        result = self.pathway.get_overlapping_dates(
            self.patient, self.episode
        )
        self.assertEqual(
            result, []
        )

    def test_get_overlapping_dates_with_no_other_episodes(self):
        self.other_episode.delete()
        result = self.pathway.get_overlapping_dates(
            self.patient, self.episode
        )
        self.assertEqual(
            result, []
        )

    def test_get_further_treatment_information_with_result(self):
        self.other_episode.fp17treatmentcategory_set.update(
            treatment_category=models.Fp17TreatmentCategory.BAND_1
        )
        self.other_episode.fp17incompletetreatment_set.update(
            date_of_acceptance=self.date_1,
            completion_or_last_visit=self.date_2
        )
        result = self.pathway.get_further_treatment_information(
            self.patient, self.episode
        )
        self.assertEqual(
            result, [{
                "category": models.Fp17TreatmentCategory.BAND_1,
                "completion_or_last_visit": self.date_2
            }]
        )

    def test_get_further_treatment_information_with_urgent_treatment(self):
        self.other_episode.fp17treatmentcategory_set.update(
            treatment_category=models.Fp17TreatmentCategory.URGENT_TREATMENT
        )
        self.other_episode.fp17incompletetreatment_set.update(
            date_of_acceptance=self.date_1,
            completion_or_last_visit=self.date_2
        )
        result = self.pathway.get_further_treatment_information(
            self.patient, self.episode
        )
        self.assertEqual(
            result, []
        )

    def test_get_further_treatment_with_information_with_incomplete_treatment(self):
        self.other_episode.fp17treatmentcategory_set.update(
            treatment_category=models.Fp17TreatmentCategory.BAND_1
        )
        self.other_episode.fp17incompletetreatment_set.update(
            date_of_acceptance=self.date_1,
            completion_or_last_visit=self.date_2,
            incomplete_treatment=models.Fp17IncompleteTreatment.BAND_1
        )
        result = self.pathway.get_further_treatment_information(
            self.patient, self.episode
        )
        self.assertEqual(
            result, []
        )

    def test_get_free_repair_replacement_information(self):
        self.other_episode.fp17treatmentcategory_set.update(
            treatment_category=models.Fp17TreatmentCategory.BAND_1
        )
        self.other_episode.fp17incompletetreatment_set.update(
            completion_or_last_visit=self.date_1,
            incomplete_treatment=models.Fp17IncompleteTreatment.BAND_1
        )
        result = self.pathway.get_free_repair_replacement_information(
            self.patient, self.episode
        )
        self.assertEqual(
            result, [{
                "category": models.Fp17TreatmentCategory.BAND_1,
                "completion_or_last_visit": self.date_1,
            }]
        )

    def test_get_further_treatment_with_information_with_no_other_episodes(self):
        self.other_episode.delete()
        result = self.pathway.get_further_treatment_information(
            self.patient, self.episode
        )
        self.assertEqual(
            result, []
        )

    def test_pathway_get(self):
        self.other_episode.fp17treatmentcategory_set.update(
            treatment_category=models.Fp17TreatmentCategory.BAND_1
        )
        self.other_episode.fp17incompletetreatment_set.update(
            date_of_acceptance=self.date_1,
            completion_or_last_visit=self.date_2
        )
        result = self.client.get(self.url).json()['steps'][-1]
        self.assertEqual(result["overlapping_dates"], [['04/10/2019', '05/10/2019']])
        self.assertEqual(
            result["further_treatment_information"],
            [{
                "category": models.Fp17TreatmentCategory.BAND_1,
                "completion_or_last_visit": '05/10/2019'
            }]
        )
        self.assertEqual(
            result["free_repair_replacement_information"],
            [{
                "category": models.Fp17TreatmentCategory.BAND_1,
                "completion_or_last_visit": '05/10/2019'
            }]
        )


    def test_episode_submitted(self):
        self.episode.submission_set.create(
            state="SUCCESS"
        )
        result = self.client.get(self.url).json()['steps'][-1]
        self.assertTrue(result["episode_submitted"])

    def test_episode_not_submitted(self):
        result = self.client.get(self.url).json()['steps'][-1]
        self.assertFalse(result["episode_submitted"])


class Fp17_O_PathwayTestCase(OpalTestCase):

    def test_save_sets_stage(self):
        patient, episode = self.new_patient_and_episode_please()
        pathway = pathways.Fp17OPathway()
        fp17_o = patient.create_episode(category_name='FP17O', stage='New')
        pathway.save({}, patient=patient, episode=fp17_o)
        fp17_o = Episode.objects.get(pk=fp17_o.pk)
        self.assertEqual('Open', fp17_o.stage)


class SubmitFP17OPathwayTestCase(OpalTestCase):
    def setUp(self):
        self.patient, self.episode = self.new_patient_and_episode_please()
        self.other_episode = self.patient.create_episode(
            stage=episode_categories.FP17OEpisode.SUBMITTED
        )
        self.date_1 = datetime.date(2019, 10, 4)
        self.date_2 = datetime.date(2019, 10, 5)
        self.date_3 = datetime.date(2019, 10, 6)
        self.assertTrue(
            self.client.login(
                username=self.user.username, password=self.PASSWORD
            )
        )
        self.url = reverse(
            "pathway", kwargs=dict(
                name="fp17-o-submit",
                patient_id=self.patient.id,
                episode_id=self.episode.id
            )
        )

    def test_with_overlapping_dates_singular(self):
        self.other_episode.orthodonticassessment_set.update(
            date_of_assessment=self.date_1
        )
        result = self.client.get(self.url)
        self.assertEqual(
            result.json()['steps'][-1]["overlapping_dates"],
            [{
                "dates": ['04/10/2019'],
                "completion_type": None

            }]
        )

    def test_with_two_overlapping_dates(self):
        self.other_episode.orthodonticassessment_set.update(
            date_of_appliance_fitted=self.date_1
        )
        self.other_episode.orthodontictreatment_set.update(
            date_of_completion=self.date_2
        )
        result = self.client.get(self.url)
        self.assertEqual(
            result.json()['steps'][-1]["overlapping_dates"],
            [{
                "dates": ['04/10/2019', '05/10/2019'],
                "completion_type": None

            }]
        )

    def test_with_three_overlapping_dates(self):
        self.other_episode.orthodonticassessment_set.update(
            date_of_assessment=self.date_1,
            date_of_appliance_fitted=self.date_2
        )
        self.other_episode.orthodontictreatment_set.update(
            date_of_completion=self.date_3
        )
        result = self.client.get(self.url)
        self.assertEqual(
            result.json()['steps'][-1]["overlapping_dates"],
            [{
                "dates": ['04/10/2019', '06/10/2019'],
                "completion_type": None

            }]
        )

    def test_no_overlapping_dates(self):
        result = self.client.get(self.url)
        self.assertEqual(
            result.json()['steps'][-1]["overlapping_dates"],
            []
        )

    def test_overlapping_dates_with_treatment(self):
        self.other_episode.orthodonticassessment_set.update(
            date_of_assessment=self.date_1
        )
        self.other_episode.orthodontictreatment_set.update(
            completion_type=models.OrthodonticTreatment.TREATMENT_COMPLETED
        )
        result = self.client.get(self.url)
        self.assertEqual(
            result.json()['steps'][-1]["overlapping_dates"],
            [{"dates": ['04/10/2019'], "completion_type": models.OrthodonticTreatment.TREATMENT_COMPLETED}]
        )

    def test_with_multiple_other_episodes(self):
        other_episode_2 = self.patient.create_episode(
            stage=episode_categories.FP17OEpisode.SUBMITTED
        )
        other_episode_2.orthodontictreatment_set.update(
            date_of_completion=self.date_1
        )
        self.other_episode.orthodonticassessment_set.update(
            date_of_assessment=self.date_2
        )
        result = self.client.get(self.url)
        self.assertEqual(
            result.json()['steps'][-1]["overlapping_dates"],
            [
                {"dates": ['05/10/2019'], "completion_type": None},
                {"dates": ['04/10/2019'], "completion_type": None}
            ]
        )

    def test_other_assessments(self):
        appliance_fitted = models.OrthodonticAssessment.ASSESS_AND_APPLIANCE_FITTED
        self.other_episode.orthodonticassessment_set.update(
            date_of_assessment=self.date_1,
            assessment=appliance_fitted
        )
        self.other_episode.category_name = episode_categories.FP17OEpisode.display_name
        self.other_episode.stage = episode_categories.FP17OEpisode.SUBMITTED
        self.other_episode.save()
        other_episode_2 = self.patient.episode_set.create(
            category_name=episode_categories.FP17OEpisode.display_name,
            stage=episode_categories.FP17OEpisode.SUBMITTED
        )
        other_episode_2.orthodontictreatment_set.update(
            date_of_completion=self.date_2,
            completion_type=models.OrthodonticTreatment.TREATMENT_COMPLETED
        )
        result = self.client.get(self.url)
        self.assertEqual(
            result.json()['steps'][-1]["other_assessments"],
            [
                {"date": '04/10/2019', "assessment": appliance_fitted},
                {"date": '05/10/2019', "assessment": None},
            ]
        )

    def test_episode_submitted(self):
        self.episode.submission_set.create(
            state="SUCCESS"
        )
        result = self.client.get(self.url).json()['steps'][-1]
        self.assertTrue(result["episode_submitted"])

    def test_episode_not_submitted(self):
        result = self.client.get(self.url).json()['steps'][-1]
        self.assertFalse(result["episode_submitted"])


class SubmitCovidTriagePathwayTestCase(OpalTestCase):
    def setUp(self):
        self.patient, self.episode = self.new_patient_and_episode_please()
        self.episode.category_name = episode_categories.CovidTriageEpisode.display_name

        self.assertTrue(
            self.client.login(
                username=self.user.username, password=self.PASSWORD
            )
        )
        self.url = reverse(
            "pathway", kwargs=dict(
                name="covid-triage-submit",
                patient_id=self.patient.id,
                episode_id=self.episode.id
            )
        )

    def test_other_triage(self):
        other_episode = self.patient.create_episode(
            category_name=episode_categories.CovidTriageEpisode.display_name,
            stage=episode_categories.CovidTriageEpisode.SUBMITTED
        )
        other_episode.covidtriage_set.update(
            datetime_of_contact=datetime.datetime(2020, 10, 4, 12, 30),
        )
        result = self.client.get(self.url)
        self.assertEqual(
            result.json()['steps'][-1]["other_triage"],
            ['04/10/2020 12:30:00']
        )

    def test_no_other_triage(self):
        result = self.client.get(self.url)
        self.assertEqual(
            result.json()['steps'][-1]["other_triage"], []
        )
