"""
New episode category setup
"""
from django.core.management.base import BaseCommand

from opal.models import Patient

class Command(BaseCommand):
    def handle(self, *a, **k):
        for patient in Patient.objects.all():

            for episode in patient.episode_set.all():
                if episode.stage == 'New':
                    pass # It's untouched, leave it as a dental care episode

                elif episode.stage == 'Open Orthodontic':
                    episode.category_name = 'FP17O'
                    episode.stage = 'Open'
                    episode.save()

                elif episode.stage in ['Open', 'Submitted']:
                    episode.category_name = 'FP17'
                    episode.save()

                elif episode.stage == None:
                    if episode.category_name == 'Dental Care':
                        pass # This is another way to spell an untouched episode - leave it be

                else:
                    print('Problem with episode {}, patient {}'.format(episode.pk, patient.pk))


            if not patient.episode_set.filter(category_name='FP17', stage='New').exists():
                patient.create_episode(category_name='FP17', stage='New')

            if not patient.episode_set.filter(category_name='FP17O', stage='New').exists():
                patient.create_episode(category_name='FP17O', stage='New')

            if not patient.episode_set.filter(category_name="Dental Care").exists():
                patient.create_episode(category_name='Dental Care', stage='New')

        return
