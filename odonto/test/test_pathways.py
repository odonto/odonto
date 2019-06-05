"""
Unittests for odonto.pathways
"""
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
