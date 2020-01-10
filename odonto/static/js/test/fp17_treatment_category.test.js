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
      };
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
    editing.fp17_treatment_category.treatment_category = "Band 1";
    expect(Fp17TreatmentCategory(editing)).toBe(undefined);
  });
});