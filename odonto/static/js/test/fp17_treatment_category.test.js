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
});