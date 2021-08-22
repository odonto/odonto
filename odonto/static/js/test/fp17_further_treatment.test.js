describe('Fp17FurtherTreatment', function() {
  "use strict";
  var Fp17FurtherTreatment, toMomentFilter;
  var editing, step;
  var juneDate, julyDate, janDate, augDate;

  var BAND_1 = "Band 1";
  var BAND_3 = "Band 3";
  var PRESCRIPTION_ONLY = "Prescription only";

  beforeEach(module('opal.filters'));
  beforeEach(module('opal.services'));


  beforeEach(function(){
      inject(function($injector){
        Fp17FurtherTreatment  = $injector.get('Fp17FurtherTreatment');
        toMomentFilter  = $injector.get('toMomentFilter');
      });

      juneDate = toMomentFilter("01/06/2019");
      julyDate = toMomentFilter("01/07/2019");
      janDate = toMomentFilter("01/01/2019");
      augDate = toMomentFilter("01/08/2019");

      editing = {
        fp17_other_dental_services: {
          further_treatment_within_2_months: true
        },
        fp17_incomplete_treatment: {
          date_of_acceptance: julyDate
        },
        fp17_treatment_category: {
          treatment_category: BAND_1
        }
      };
      step = {
        further_treatment_information: []
      }
  });


  it('should not error if there is no further treatment', function(){
    editing.fp17_other_dental_services.further_treatment_within_2_months = false;
    expect(Fp17FurtherTreatment(editing, step)).toBe(undefined);
  });

  it('should not error if there is no date of acceptance', function(){
    editing.fp17_incomplete_treatment.date_of_acceptance = undefined;
    expect(Fp17FurtherTreatment(editing, step)).toBe(undefined);
  });

  it('should not error if there is no treatment category', function(){
    editing.fp17_treatment_category.treatment_category = undefined;
    expect(Fp17FurtherTreatment(editing, step)).toBe(undefined);
  });

  it('should error if it is not band 1, 2, or 3', function(){
    editing.fp17_treatment_category.treatment_category = PRESCRIPTION_ONLY;
    var expected = {
      fp17_other_dental_services: {
        further_treatment_within_2_months: "Requires Band 1, 2 or 3"
      }
    };
    expect(Fp17FurtherTreatment(editing, step)).toEqual(expected);
  });

  it('should error if there are no prior episodes', function(){
    var expected = {
      fp17_other_dental_services: {
        further_treatment_within_2_months: "No prior episode found in the last two months"
      }
    };
    expect(Fp17FurtherTreatment(editing, step)).toEqual(expected);
  });

  it('should error if there are prior episodes but they are over 2 months ago', function(){
    step.further_treatment_information = [{
      category: BAND_1,
      completion_or_last_visit: janDate
    }];

    var expected = {
      fp17_other_dental_services: {
        further_treatment_within_2_months: "No prior episode found in the last two months"
      }
    };
    expect(Fp17FurtherTreatment(editing, step)).toEqual(expected);
  });

  it('should error if other episodes are in the future', function(){
    step.further_treatment_information = [{
      category: BAND_1,
      completion_or_last_visit: augDate
    }];

    var expected = {
      fp17_other_dental_services: {
        further_treatment_within_2_months: "No prior episode found in the last two months"
      }
    };
    expect(Fp17FurtherTreatment(editing, step)).toEqual(expected);
  });

  it('should not error if there is a previous episode with a higher band', function(){
    step.further_treatment_information = [{
      category: BAND_3,
      completion_or_last_visit: juneDate
    }];

    expect(Fp17FurtherTreatment(editing, step)).toBe(undefined)
  });

  it('should error are there no other episodes are of a higher band', function(){
    editing.fp17_treatment_category.treatment_category = BAND_3;
    step.further_treatment_information = [{
      category: BAND_1,
      completion_or_last_visit: juneDate
    }];

    var expected = {
      fp17_other_dental_services: {
        further_treatment_within_2_months: "No prior episode found with an appropriate category"
      }
    };
    expect(Fp17FurtherTreatment(editing, step)).toEqual(expected)
  });

  it('should not error if other episodes are of a non band type', function(){
    editing.fp17_treatment_category.treatment_category = BAND_3;
    step.further_treatment_information = [{
      category: PRESCRIPTION_ONLY,
      completion_or_last_visit: juneDate
    }];
    expect(Fp17FurtherTreatment(editing, step)).toBe(undefined);
  });
});
