import decimal
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
        performer_number_obj = user.performernumber_set.create()
        care_provider = self.episode.fp17dentalcareprovider_set.create(
            performer=user.get_full_name(),
            provider_location_number='010108',
        )
        performer = care_provider.get_performer_obj()
        self.assertEqual(
            performer_number_obj, performer
        )

    def test_get_user_but_performer_object_does_not_exist(self):
        # for non dentists they will not have a performer obj
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
        self.assertIsNone(performer)

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


class Fp17ExemptionsToDictTestCase(OpalTestCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        _, episode = self.new_patient_and_episode_please()
        self.exemption = episode.fp17exemptions_set.get()

    def test_with_patient_charge_collected(self):
        self.exemption.patient_charge_collected = decimal.Decimal("12.05")
        self.exemption.save()
        as_dict = self.exemption.to_dict(None)
        self.assertEqual(
            as_dict["patient_charge_collected"], float(12.05)
        )

    def test_without_patient_charge_collected(self):
        self.exemption.patient_charge_collected = None
        self.exemption.save()
        as_dict = self.exemption.to_dict(None)
        self.assertEqual(
            as_dict["patient_charge_collected"], None
        )
