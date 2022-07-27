describe('Fp17TreatmentCategory', function() {
  "use strict";
  var Fp17TreatmentCategory;
  var editing;
  var expected;
  var BAND_1 = "Band 1";
  var BAND_2 = "Band 2";
  var BAND_3 = "Band 3";

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
      editing.fp17_treatment_category.treatment_category = "Urgent treatment";
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
      editing.fp17_treatment_category.treatment_category = "Band 1";
      expect(Fp17TreatmentCategory(editing)).toBe(undefined);
    });

    it('should not return an error if the treatment category is not band 1 and free_repair_or_replacement is true', function(){
      editing.fp17_treatment_category.treatment_category = "Band 2";
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
      editing.fp17_treatment_category.treatment_category = "Band 2";
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
});
