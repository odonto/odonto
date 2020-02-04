describe('Fp17DateOfAcceptance', function() {
  "use strict";
  var Fp17DateOfAcceptance;
  var editing, step;

  beforeEach(module('opal.filters'));
  beforeEach(module('opal.services'));

  var URGENT_TREATMENT = "Urgent treatment";
  var DENTURE_REPAIRS = "Denture repairs";
  var BRIDGE_REPAIRS = "Bridge repairs";

  beforeEach(function(){
    inject(function($injector){
      Fp17DateOfAcceptance  = $injector.get('Fp17DateOfAcceptance');
    });
    editing = {
      fp17_incomplete_treatment: {},
      fp17_treatment_category: {}
    };
    step = {
      overlapping_dates: []
    }
  });

  describe('date of acceptance cannot be in the future', function(){
    it('should error if the date of acceptance is not in the future', function(){
      editing.fp17_incomplete_treatment.date_of_acceptance = moment().add(2, "d").toDate();
      var result = Fp17DateOfAcceptance(editing, step);
      var error = result.fp17_incomplete_treatment.date_of_acceptance;
      expect(error).toBe("Date of acceptance cannot be in the future");
    });

    it('should not error if there is not error if date of acceptance is today', function(){
      editing.fp17_incomplete_treatment.date_of_acceptance = moment();
      var result = Fp17DateOfAcceptance(editing, step);
      expect(result).toBeUndefined();
    });
  })

  describe('if there is a concurrent episode it should error', function(){
    var day1 = moment().subtract(3, "days");
    var day2 = moment().subtract(2, "days");
    var day3 = moment().subtract(1, "days");

    it('should error if there is a concurrent surrounding episode', function(){
      step.overlapping_dates = [[day1, day2]];
      editing.fp17_incomplete_treatment.date_of_acceptance = day2;
      var result = Fp17DateOfAcceptance(editing, step);
      var error = result.fp17_incomplete_treatment.date_of_acceptance;
      expect(error).toBe("The FP17 overlaps with another FP17 of this patient");
    });

    it('should not error if it is urgent treatment', function(){
      step.overlapping_dates = [[day1, day2]];
      editing.fp17_incomplete_treatment.date_of_acceptance = day2;
      editing.fp17_treatment_category.treatment_category = URGENT_TREATMENT;
      var result = Fp17DateOfAcceptance(editing, step);
      expect(result).toBeUndefined()
    });

    it('should not error if it is denture repairs', function(){
      step.overlapping_dates = [[day1, day2]];
      editing.fp17_incomplete_treatment.date_of_acceptance = day2;
      editing.fp17_treatment_category.treatment_category = DENTURE_REPAIRS;
      var result = Fp17DateOfAcceptance(editing, step);
      expect(result).toBeUndefined()
    });

    it('should not error if it is bridge repairs', function(){
      step.overlapping_dates = [[day1, day2]];
      editing.fp17_incomplete_treatment.date_of_acceptance = day2;
      editing.fp17_treatment_category.treatment_category = BRIDGE_REPAIRS;
      var result = Fp17DateOfAcceptance(editing, step);
      expect(result).toBeUndefined();
    });

    it('should not error if the concurrent episode does not overlap', function(){
      step.overlapping_dates = [[day1, day2]];
      editing.fp17_incomplete_treatment.date_of_acceptance = day3;
      var result = Fp17DateOfAcceptance(editing, step);
      expect(result).toBeUndefined();
    });
  });
});