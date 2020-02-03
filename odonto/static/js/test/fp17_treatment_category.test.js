describe('Fp17TreatmentCategory', function() {
  "use strict";
  var Fp17TreatmentCategory;
  var editing;
  var expected;

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
          treatment_category: "The incomplete treatment band cannot be greater than the treatment category"
        },
      };
    });

    it('should not error if the treatment category is urgent', function(){
      editing.fp17_treatment_category.treatment_category = "Urgent treatment";
      editing.fp17_incomplete_treatment.incomplete_treatment = "Band 1";
      expect(Fp17TreatmentCategory(editing)).toBe(undefined);
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

    it('should error if the band is higher than the incomplete treatment for band 1', function(){
      editing.fp17_treatment_category.treatment_category = "Band 1";
      editing.fp17_incomplete_treatment.incomplete_treatment = "Band 3";
      expect(Fp17TreatmentCategory(editing)).toEqual(expected);

      editing.fp17_treatment_category.treatment_categorecty = "Band 1";
      editing.fp17_incomplete_treatment.incomplete_treatment = "Band 2";
      expect(Fp17TreatmentCategory(editing)).toEqual(expected);
    });

    it('should error if the band is higher than the incomplete treatment for band 2', function(){
      editing.fp17_treatment_category.treatment_category = "Band 2";
      editing.fp17_incomplete_treatment.incomplete_treatment = "Band 3";
      expect(Fp17TreatmentCategory(editing)).toEqual(expected);
    });
  })
});