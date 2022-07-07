describe('Fp17TreatmentCategory', function() {
  "use strict";
  var Fp17TreatmentCategory;
  var editing;

  var expected;
  var BAND_1 = "Band 1";
  var BAND_2 = "Band 2";
  var BAND_3 = "Band 3";
  var URGENT_TREATMENT = "Urgent treatment";
  var REGULATION_11_REPLACEMENT_APPLIANCE = "Regulation 11 replacement appliance";
  var BRIDGE_REPAIRS = "Bridge repairs"

  beforeEach(module('opal.filters'));
  beforeEach(module('opal.services'));

  beforeEach(function(){
      inject(function($injector){
        Fp17TreatmentCategory  = $injector.get('Fp17TreatmentCategory');
      });

      editing = {

        fp17_treatment_category: {
          treatment_category: undefined
        },
        fp17_clinical_data_set: {
          examination: true
        },
        fp17_other_dental_services: {
          free_repair_or_replacement: false,
          further_treatment_within_2_months: false
        },
        fp17_incomplete_treatment: {
          fp17_incomplete_treatment: undefined
        },
        fp17_exemptions: {
          patient_charge_collected: undefined
        }
      };
  });

  describe("Treatment category is required", function(){
    beforeEach(function(){
      expected = {
        fp17_treatment_category: {
          treatment_category: "Treatment category is required"
        },
      };
    });

    it('should return an error message if treatment category is an empty string', function(){
      editing.fp17_treatment_category.treatment_category = "";

      expect(Fp17TreatmentCategory(editing)).toEqual(expected);

    });


    it('should return an error message if treatment category is undefined', function(){
      expect(Fp17TreatmentCategory(editing)).toEqual(expected);

    });

    it('should not return an error message if treatment category is set', function(){
      editing.fp17_treatment_category.treatment_category = BAND_1;

      expect(Fp17TreatmentCategory(editing)).toBe(undefined);

    });
  });

  describe("A patient cannot have band 1 and free repair or replacement", function(){
    beforeEach(function(){
      expected = {
        fp17_treatment_category: {
          treatment_category: "A patient cannot have band 1 and free repair or replacement"
        },
      };
    });

    it('should return an error if the treatment category is band 1 and free_repair_or_replacement is true', function(){
      editing.fp17_treatment_category.treatment_category = "Band 1";

      editing.fp17_other_dental_services.free_repair_or_replacement = true;

      expect(Fp17TreatmentCategory(editing)).toEqual(expected);

    });

    it('should not return an error if the treatment category is band 1 and free_repair_or_replacement is false', function(){
      editing.fp17_treatment_category.treatment_category = BAND_1;


      // band 1 needs a CDS of band 1
      editing.fp17_clinical_data_set.examination = true

      expect(Fp17TreatmentCategory(editing)).toBe(undefined);

    });

    it('should not return an error if the treatment category is not band 1 and free_repair_or_replacement is true', function(){
      editing.fp17_treatment_category.treatment_category = "Band 2";


      // band 2 requires a cds of band 2
      editing.fp17_clinical_data_set.endodontic_treatment = true;

      editing.fp17_other_dental_services.free_repair_or_replacement = true;

      expect(Fp17TreatmentCategory(editing)).toBe(undefined);

    });
  });

  describe("A patient cannot have a free repair or replacement without a prior claim of an equal or higher band", function(){
    var step;
    beforeEach(function(){
      expected = {
        fp17_treatment_category: {
          treatment_category: "Free repair or replacement requires a band equal or lower to a previous treatment in the last 12 months"
        },
      };
      step = {free_repair_replacement_information: []};
    });

    it("should error if there is no prior claim", function(){
      editing.fp17_treatment_category.treatment_category = BAND_2;

      editing.fp17_other_dental_services.free_repair_or_replacement = true;

      editing.fp17_incomplete_treatment.completion_or_last_visit = new Date(2021, 6, 6);

      expect(Fp17TreatmentCategory(editing, step)).toEqual(expected);

    });

    it("should error if there is a prior claim that is of a lower band", function(){
      editing.fp17_treatment_category.treatment_category = BAND_2;

      editing.fp17_other_dental_services.free_repair_or_replacement = true;

      editing.fp17_incomplete_treatment.completion_or_last_visit = new Date(2021, 6, 6);

      step.free_repair_replacement_information.push({
        category: BAND_1,
        completion_or_last_visit: new Date(2021, 6, 5)
      })
      expect(Fp17TreatmentCategory(editing, step)).toEqual(expected);

    });

    it("should error if there is a future claim of a higher band", function(){
      editing.fp17_treatment_category.treatment_category = BAND_2;

      editing.fp17_other_dental_services.free_repair_or_replacement = true;

      editing.fp17_incomplete_treatment.completion_or_last_visit = new Date(2021, 6, 6);

      step.free_repair_replacement_information.push({
        category: BAND_3,
        completion_or_last_visit: new Date(2021, 6, 7)
      })
      expect(Fp17TreatmentCategory(editing, step)).toEqual(expected);

    });

    it("should error if there is a previous claim of a higher band more than a year ago", function(){
      editing.fp17_treatment_category.treatment_category = BAND_2;

      editing.fp17_other_dental_services.free_repair_or_replacement = true;

      editing.fp17_incomplete_treatment.completion_or_last_visit = new Date(2021, 6, 6);

      step.free_repair_replacement_information.push({
        category: BAND_3,
        completion_or_last_visit: new Date(2020, 6, 5)
      })
      expect(Fp17TreatmentCategory(editing, step)).toEqual(expected);

    });

    it("should not error if the claim is band 2 and there is a previous claim of band 2", function(){
      editing.fp17_treatment_category.treatment_category = BAND_2;


      // band 2 require a CDS of band 2
      editing.fp17_clinical_data_set.endodontic_treatment = true;

      editing.fp17_other_dental_services.free_repair_or_replacement = true;

      editing.fp17_incomplete_treatment.completion_or_last_visit = new Date(2021, 6, 6);

      step.free_repair_replacement_information.push({
        category: BAND_2,
        completion_or_last_visit: new Date(2020, 6, 6)
      })
      expect(Fp17TreatmentCategory(editing, step)).toBe(undefined);

    });

    it("should not error if the claim is band 2 and there is a previous claim of band 3", function(){
      editing.fp17_treatment_category.treatment_category = BAND_2;

      // band 2 require a CDS of band 2
      editing.fp17_clinical_data_set.endodontic_treatment = true;

      editing.fp17_other_dental_services.free_repair_or_replacement = true;

      editing.fp17_incomplete_treatment.completion_or_last_visit = new Date(2021, 6, 6);

      step.free_repair_replacement_information.push({
        category: BAND_3,
        completion_or_last_visit: new Date(2020, 6, 6)
      })
      expect(Fp17TreatmentCategory(editing, step)).toBe(undefined);

    });

    it("should not error if the claim is band 3 and there is a previous claim of band 3", function(){
      editing.fp17_treatment_category.treatment_category = BAND_3;

      // band 2 require a CDS of band 2
      editing.fp17_clinical_data_set.crowns_provided = 1;

      editing.fp17_other_dental_services.free_repair_or_replacement = true;

      editing.fp17_incomplete_treatment.completion_or_last_visit = new Date(2021, 6, 6);

      step.free_repair_replacement_information.push({
        category: BAND_3,
        completion_or_last_visit: new Date(2020, 6, 6)
      })
      expect(Fp17TreatmentCategory(editing, step)).toBe(undefined);

    });
  });

  describe("A patient cannot have urgent treatment and further treatment within 2 months", function(){
    beforeEach(function(){
      expected = {
        fp17_treatment_category: {
          treatment_category: "A patient cannot have urgent treatment and further treatment within 2 months"
        },
      };
    });

    it('should return an error if the treatment category is urgent treatment and further_treatment_within_2_months is true', function(){
      editing.fp17_treatment_category.treatment_category = "Urgent treatment";

      editing.fp17_other_dental_services.further_treatment_within_2_months = true;

      expect(Fp17TreatmentCategory(editing)).toEqual(expected);

    });

    it('should not return an error if the treatment category is urgent treatment and further_treatment_within_2_months is false', function(){
      editing.fp17_treatment_category.treatment_category = "Urgent treatment";

      expect(Fp17TreatmentCategory(editing)).toBe(undefined);

    });

    it('should not return an error if the treatment category is not urgent treatment and further_treatment_within_2_months is true', function(){
      editing.fp17_treatment_category.treatment_category = BAND_1;

      editing.fp17_other_dental_services.further_treatment_within_2_months = true;

      expect(Fp17TreatmentCategory(editing)).toBe(undefined);

    });
  });

  describe("A patient cannot have an incomplete treatment band higher than the treatment category", function(){
    beforeEach(function(){
      expected = {
        fp17_treatment_category: {
          treatment_category: "The incomplete treatment band cannot be greater than the treatment category band"
        },
      };
    });

    it('should not error if incomplete treatment and treatment category are band 1', function(){
      editing.fp17_treatment_category.treatment_category = "Band 1";

      editing.fp17_incomplete_treatment.incomplete_treatment = "Band 1";

      expect(Fp17TreatmentCategory(editing)).toBe(undefined);

    });

    it('should not error if incomplete treatment and treatment category are band 2', function(){
      editing.fp17_treatment_category.treatment_category = "Band 2";


      // band 2 requires a cds of band 2
      editing.fp17_clinical_data_set.endodontic_treatment = 2;

      editing.fp17_incomplete_treatment.incomplete_treatment = "Band 2";

      expect(Fp17TreatmentCategory(editing)).toBe(undefined);

    });

    it('should not error if the band is urgent treatment and the incomplete treatment is band 2', function(){
      var err = "The incomplete treatment band cannot be greater than the treatment category band"
      expected.fp17_treatment_category.treatment_category = err;
      editing.fp17_treatment_category.treatment_category = "Band 1";

      editing.fp17_incomplete_treatment.incomplete_treatment = "Band 2";

      expect(Fp17TreatmentCategory(editing)).toEqual(expected);

    });

    it('should error if the band is higher than the incomplete treatment for band 1', function(){
      editing.fp17_treatment_category.treatment_category = "Band 1";

      editing.fp17_incomplete_treatment.incomplete_treatment = "Band 3";

      expect(Fp17TreatmentCategory(editing)).toEqual(expected);


      editing.fp17_treatment_category.treatment_category = "Band 1";

      editing.fp17_incomplete_treatment.incomplete_treatment = "Band 2";

      expect(Fp17TreatmentCategory(editing)).toEqual(expected);

    });

    it('should error if the band is higher than the incomplete treatment for band 2', function(){
      editing.fp17_treatment_category.treatment_category = "Band 2";

      editing.fp17_incomplete_treatment.incomplete_treatment = "Band 3";

      expect(Fp17TreatmentCategory(editing)).toEqual(expected);

    });
  })

  describe('A patient cannot have an incomplete treatment and a treatment category of Urgent treatment', function(){
    it('should not error if incomplete treatment and treatment category are band 1', function(){
      editing.fp17_treatment_category.treatment_category = "Band 1";

      editing.fp17_incomplete_treatment.incomplete_treatment = "Band 1";

      expect(Fp17TreatmentCategory(editing)).toBe(undefined);

    });

    it('should error if the band is urgent treatment and the incomplete treatment is band 1', function(){
      expected = {
        fp17_treatment_category: {
          treatment_category: "Urgent treatment cannot have an incomplete treatment"
        }
      };
      editing.fp17_treatment_category.treatment_category = "Urgent treatment";

      editing.fp17_incomplete_treatment.incomplete_treatment = "Band 1";

      expect(Fp17TreatmentCategory(editing)).toEqual(expected);

    });
  });

  describe('regulation 11', function(){
    it('should not error if there is a charge', function(){
      editing.fp17_treatment_category.treatment_category="Regulation 11 replacement appliance"

      editing.fp17_exemptions.patient_charge_collected = 10;

      expect(Fp17TreatmentCategory(editing)).toBe(undefined);

    });

    it('should error if there is not a charge', function(){
      expected = {
        fp17_treatment_category: {
          treatment_category: "A patient charge is required for reg 11"
        }
      };
      editing.fp17_treatment_category.treatment_category="Regulation 11 replacement appliance"

      expect(Fp17TreatmentCategory(editing)).toEqual(expected);

    });
  });

  describe('A patient should have a band of the highest CDS treatment band', function(){
    beforeEach(function(){
      editing.fp17_clinical_data_set.examination = false;
    });

    function getError(err){
      return {
        fp17_treatment_category: {
          treatment_category: err
        }
      }
    }

    it('should not error if there is a referral for advanced mandetory treatment', function(){
      editing.fp17_clinical_data_set.referral_for_advanced_mandatory_services_band = 1

      editing.fp17_treatment_category.treatment_category = BAND_1;


      // a band 3 treatment
      editing.fp17_clinical_data_set.veneers_applied = 2

      expect(Fp17TreatmentCategory(editing)).toBe(undefined);

    });

    it('should error if there is an urgent treatment but no bands above 0', function(){
      editing.fp17_treatment_category.treatment_category = URGENT_TREATMENT;


      // a band 3 treatment
      editing.fp17_clinical_data_set.veneers_applied = 2

      var expected = getError('Veneers applied requires a band 3')
      expect(Fp17TreatmentCategory(editing)).toEqual(expected);

    });

    it('should not error if there is an urgent treatment and there are bands 1, or 2', function(){
      editing.fp17_treatment_category.treatment_category = URGENT_TREATMENT;


      // a band 1 treatment
      editing.fp17_clinical_data_set.other_treatment = true

      expect(Fp17TreatmentCategory(editing)).toBe(undefined);


      // a band 2 treatment
      editing.fp17_clinical_data_set.endodontic_treatment = 2

      expect(Fp17TreatmentCategory(editing)).toBe(undefined);

    });

    it('should not error if there is a regulation 11 and bands 1, 2, or 3', function(){
      editing.fp17_treatment_category.treatment_category = REGULATION_11_REPLACEMENT_APPLIANCE;


      // required for reg 11
      editing.fp17_exemptions.patient_charge_collected = 2;


      // a band 1 treatment
      editing.fp17_clinical_data_set.other_treatment = true

      expect(Fp17TreatmentCategory(editing)).toBe(undefined);


      // a band 2 treatment
      editing.fp17_clinical_data_set.endodontic_treatment = 2

      expect(Fp17TreatmentCategory(editing)).toBe(undefined);


      // a band 3 treatment
      editing.fp17_clinical_data_set.veneers_applied = 2

      expect(Fp17TreatmentCategory(editing)).toBe(undefined);

    });

    it('should not error treatment band 1 if the highest treatment is band 1', function(){
      editing.fp17_treatment_category.treatment_category = BAND_1;
      editing.fp17_clinical_data_set.other_treatment = true
      expect(Fp17TreatmentCategory(editing)).toBe(undefined);
    });

    it('should error if there is a band 1 treatment and no CDS band 1', function(){
      editing.fp17_treatment_category.treatment_category = BRIDGE_REPAIRS;
      editing.fp17_clinical_data_set.other_treatment = true
      expected = getError('Other treatment requires a band 1');
      expect(Fp17TreatmentCategory(editing)).toEqual(expected);
    });

    it('should error if there it is marked as band 1 but there is nothing recorded in the clinical dataset', function(){
      editing.fp17_treatment_category.treatment_category = BAND_1;
      expected = getError(
        "To justify a band 1, at least one of the following is required: examination, scale and_polish, fluoride varnish, fissure sealants, radiographs taken, phased treatment, other treatment"
      );
      expect(Fp17TreatmentCategory(editing)).toEqual(expected);
    });

    it('should error if there it is marked as band 1 but there are only null treatments in the clincial dataset', function(){
      editing.fp17_treatment_category.treatment_category = BAND_1;
      editing.fp17_clinical_data_set.best_practice_prevention = true
      expected = getError(
        "To justify a band 1, at least one of the following is required: examination, scale and_polish, fluoride varnish, fissure sealants, radiographs taken, phased treatment, other treatment"
      );
      expect(Fp17TreatmentCategory(editing)).toEqual(expected);
    });

    it('should not error treatment band 2 if the highest treatment is band 2', function(){
      editing.fp17_treatment_category.treatment_category = BAND_2
      // a band 2 treatment
      editing.fp17_clinical_data_set.endodontic_treatment = 2
      // a band 1 treatment
      editing.fp17_clinical_data_set.other_treatment = true;
      expect(Fp17TreatmentCategory(editing)).toBe(undefined);
    });

    it('should error if there is a band 2 treatment and no CDS band 2', function(){
      editing.fp17_treatment_category.treatment_category = BAND_2
      // a band 1 treatment
      editing.fp17_clinical_data_set.other_treatment = true;

      var expected = getError('To justify a band 2, at least one of the following is required: endodontic treatment, permanent fillings, extractions, pre formed_crowns, advanced perio_root_surface_debridement, denture additions_reline_rebase');
      expect(Fp17TreatmentCategory(editing)).toEqual(expected);
    });

    it('should not error treatment band 3 if the highest treatment is band 3', function(){
      editing.fp17_treatment_category.treatment_category = BAND_3
      // a band 3 treatment
      editing.fp17_clinical_data_set.veneers_applied = 2

      expect(Fp17TreatmentCategory(editing)).toBe(undefined);
    });

    it('should error if there is a band 3 treatment and no CDS band 3', function(){
      editing.fp17_treatment_category.treatment_category = BAND_1;

      // a band 3 treatment
      editing.fp17_clinical_data_set.veneers_applied = 2
      expected = getError('Veneers applied requires a band 3')
      expect(Fp17TreatmentCategory(editing)).toEqual(expected);

    });

    it('should error if there is a band 3 treatment and band urgent treatment', function(){
      editing.fp17_treatment_category.treatment_category = URGENT_TREATMENT;

      // a band 3 treatment
      editing.fp17_clinical_data_set.veneers_applied = 2
      expected = getError('Veneers applied requires a band 3')
      expect(Fp17TreatmentCategory(editing)).toEqual(expected);
    });

  });
});
