"""
Unittests for odonto.pathways
"""
import datetime
from django.urls import reverse
from opal.models import Episode
from opal.core.test import OpalTestCase

from odonto import pathways


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
        self.other_episode = self.patient.create_episode()
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

    def test_with_other_dates_singular(self):
        self.other_episode.orthodonticassessment_set.update(
            date_of_assessment=self.date_1
        )
        result = self.client.get(self.url)
        self.assertEqual(
            result.json()['steps'][-1]["other_dates"],
            [['04/10/2019']]
        )

    def test_with_two_other_dates(self):
        self.other_episode.orthodonticassessment_set.update(
            date_of_appliance_fitted=self.date_1
        )
        self.other_episode.orthodontictreatment_set.update(
            date_of_completion=self.date_2
        )
        result = self.client.get(self.url)
        self.assertEqual(
            result.json()['steps'][-1]["other_dates"],
            [['04/10/2019', '05/10/2019']]
        )

    def test_with_three_other_dates(self):
        self.other_episode.orthodonticassessment_set.update(
            date_of_assessment=self.date_1,
            date_of_appliance_fitted=self.date_2
        )
        self.other_episode.orthodontictreatment_set.update(
            date_of_completion=self.date_3
        )
        result = self.client.get(self.url)
        self.assertEqual(
            result.json()['steps'][-1]["other_dates"],
            [['04/10/2019', '06/10/2019']]
        )

    def test_no_other_dates(self):
        result = self.client.get(self.url)
        self.assertEqual(
            result.json()['steps'][-1]["other_dates"],
            []
        )

    def test_with_multiple_other_episodes(self):
        other_episode_2 = self.patient.create_episode()
        other_episode_2.orthodontictreatment_set.update(
            date_of_completion=self.date_1
        )
        self.other_episode.orthodonticassessment_set.update(
            date_of_assessment=self.date_2
        )
        result = self.client.get(self.url)
        self.assertEqual(
            result.json()['steps'][-1]["other_dates"],
            [['05/10/2019'], ['04/10/2019']]
        )
