import decimal
import datetime
from unittest import mock
from django.contrib.auth.models import User
from opal.core.test import OpalTestCase
from odonto import episode_categories


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


class ExtractChartTestCase(OpalTestCase):
    def setUp(self, *args, **kwargs):
        _, episode = self.new_patient_and_episode_please()
        self.extraction_chart = episode.extractionchart_set.get()

    def test_has_extractions(self):
        fields = [
            "ur_1",
            "ur_2",
            "ur_3",
            "ur_4",
            "ur_5",
            "ur_6",
            "ur_7",
            "ur_8",
            "ur_9",
            "ur_a",
            "ur_b",
            "ur_c",
            "ur_d",
            "ur_e",
            "ul_1",
            "ul_2",
            "ul_3",
            "ul_4",
            "ul_5",
            "ul_6",
            "ul_7",
            "ul_8",
            "ul_9",
            "ul_a",
            "ul_b",
            "ul_c",
            "ul_d",
            "ul_e",
            "lr_1",
            "lr_2",
            "lr_3",
            "lr_4",
            "lr_5",
            "lr_6",
            "lr_7",
            "lr_8",
            "lr_9",
            "lr_a",
            "lr_b",
            "lr_c",
            "lr_d",
            "lr_e",
            "ll_1",
            "ll_2",
            "ll_3",
            "ll_4",
            "ll_5",
            "ll_6",
            "ll_7",
            "ll_8",
            "ll_9",
            "ll_a",
            "ll_b",
            "ll_c",
            "ll_d",
            "ll_e",
        ]

        self.assertFalse(self.extraction_chart.has_extractions())

        for field in fields:
            setattr(self.extraction_chart, field, True)
            self.extraction_chart.save()
            self.assertTrue(self.extraction_chart.has_extractions())
            setattr(self.extraction_chart, field, False)
            self.extraction_chart.save()


class DemographicsTestCase(OpalTestCase):
    def setUp(self):
        patient, _ = self.new_patient_and_episode_please()
        self.demographics = patient.demographics()

    @mock.patch("odonto.models.datetime")
    def test_age(self, dt):
        dt.date.today.return_value = datetime.date(2019, 12, 1)
        self.demographics.date_of_birth = datetime.date(1990, 12, 1)
        self.assertEqual(self.demographics.get_age(), 29)
        self.assertEqual(
            self.demographics.get_age(datetime.date(2009, 11, 30)),
            18
        )
        self.assertEqual(
            self.demographics.get_age(datetime.date(2009, 12, 1)),
            19
        )
        self.assertEqual(
            self.demographics.get_age(datetime.date(2009, 12, 2)),
            19
        )

        self.demographics.date_of_birth = datetime.date(1990, 12, 10)
        self.assertEqual(
            self.demographics.get_age(datetime.date(2009, 12, 9)),
            18
        )
        self.assertEqual(
            self.demographics.get_age(datetime.date(2009, 11, 19)),
            18
        )
        self.assertEqual(
            self.demographics.get_age(datetime.date(2009, 12, 10)),
            19
        )


class Fp17TreatmentCategoryTestCase(OpalTestCase):
    def setUp(self):
        _, self.episode = self.new_patient_and_episode_please()
        self.episode.category_name = episode_categories.FP17Episode.display_name
        self.episode.save()
        self.treatment_category_obj = self.episode.fp17treatmentcategory_set.get()
        self.treatment_category_obj.treatment_category = self.treatment_category_obj.BAND_2
        self.episode.fp17incompletetreatment_set.update(
          completion_or_last_visit=datetime.date(2022, 11, 22)
        )
        self.clinical_data_set = self.episode.fp17clinicaldataset_set.get()

    def test_band_2_subdivision_non_band_2(self):
        self.treatment_category_obj.treatment_category = self.treatment_category_obj.BAND_1
        with self.assertRaises(ValueError):
            self.treatment_category_obj.calculate_band_2_subdivision()

    def test_band_2_subdivision_before_start_date(self):
        self.episode.fp17incompletetreatment_set.update(
          completion_or_last_visit=datetime.date(2022, 10, 2)
        )
        self.assertEqual(
            self.treatment_category_obj.calculate_band_2_subdivision(),
            self.treatment_category_obj.BAND_2
        )

    def test_molar_endodontic_treatment(self):
        self.clinical_data_set.molar_endodontic_treatment = 1
        self.clinical_data_set.save()
        self.assertEqual(
            self.treatment_category_obj.calculate_band_2_subdivision(),
            self.treatment_category_obj.BAND_2_C
        )

    def test_non_molar_endodontic_treatment(self):
        self.clinical_data_set.molar_endodontic_treatment = 1
        self.clinical_data_set.save()
        self.assertEqual(
            self.treatment_category_obj.calculate_band_2_subdivision(),
            self.treatment_category_obj.BAND_2_C
        )

    def test_permanent_fillings_and_extracts(self):
        # test with none attributes in permanent fillings or extractions
        self.clinical_data_set.permanent_fillings = 3
        self.clinical_data_set.save()
        self.assertEqual(
            self.treatment_category_obj.calculate_band_2_subdivision(),
            self.treatment_category_obj.BAND_2_B
        )
        self.clinical_data_set.permanent_fillings = None
        self.clinical_data_set.extractions = 3
        self.clinical_data_set.save()
        self.assertEqual(
            self.treatment_category_obj.calculate_band_2_subdivision(),
            self.treatment_category_obj.BAND_2_B
        )

        # test that they add up over 3
        self.clinical_data_set.permanent_fillings = 2
        self.clinical_data_set.extractions = 1
        self.clinical_data_set.save()
        self.assertEqual(
            self.treatment_category_obj.calculate_band_2_subdivision(),
            self.treatment_category_obj.BAND_2_B
        )

        # test that otherwise its a band 2 a
        self.clinical_data_set.permanent_fillings = 1
        self.clinical_data_set.extractions = 1
        self.clinical_data_set.save()
        self.assertEqual(
            self.treatment_category_obj.calculate_band_2_subdivision(),
            self.treatment_category_obj.BAND_2_A
        )

    def test_band_2_A(self):
        self.assertEqual(
            self.treatment_category_obj.calculate_band_2_subdivision(),
            self.treatment_category_obj.BAND_2_A
        )
