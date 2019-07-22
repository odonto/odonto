from django.contrib.auth.models import User
from opal.core.test import OpalTestCase


class GetPerformerObjectTestCase(OpalTestCase):
    def setUp(self):
        _, self.episode = self.new_patient_and_episode_please()

    def test_get_performer_object_found(self):
        user = User.objects.create(
            username="W.Flintstone",
            first_name="Wilma",
            last_name="Flintstone"
        )
        care_provider = self.episode.fp17dentalcareprovider_set.create(
            performer=user.get_full_name(),
            provider_location_number='010108',
        )
        performer = care_provider.get_performer_obj()
        self.assertEqual(
            user, performer
        )

    def test_get_performer_object_not_found(self):
        care_provider = self.episode.fp17dentalcareprovider_set.create(
            performer="someone",
            provider_location_number='010108',
        )
        performer = care_provider.get_performer_obj()
        self.assertIsNone(performer)

    def test_performer_is_none(self):
        care_provider = self.episode.fp17dentalcareprovider_set.create(
            performer=None,
            provider_location_number='010108',
        )
        performer = care_provider.get_performer_obj()
        self.assertIsNone(performer)
