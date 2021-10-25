describe('CompletionOrLastVisit', function() {
  "use strict";
  var CompletionOrLastVisit;
  var editing, step;

  beforeEach(module('opal.filters'));
  beforeEach(module('opal.services'));

  var URGENT_TREATMENT = "Urgent treatment";
  var DENTURE_REPAIRS = "Denture repairs";
  var BRIDGE_REPAIRS = "Bridge repairs";

  var day1 = moment().subtract(3, "days");
  var day2 = moment().subtract(2, "days");
  var day3 = moment().subtract(1, "days");


  beforeEach(function(){
    inject(function($injector){
      CompletionOrLastVisit  = $injector.get('CompletionOrLastVisit');
    });
    editing = {
      fp17_incomplete_treatment: {},
      fp17_treatment_category: {}
    };
    step = {
      overlapping_dates: []
    }
  });

  describe('completion or last is mandatory', function(){
    it('should error if there is no completion_or_last_visit', function(){
      var result = CompletionOrLastVisit(editing, step);
      var error = result.fp17_incomplete_treatment.completion_or_last_visit;
      expect(error).toEqual("Date of completion or last visit is required");
    });
  });

  describe('completion or last visit cannot be in the future', function(){
    it('should error if the date of acceptance is not in the future', function(){
      editing.fp17_incomplete_treatment.completion_or_last_visit = moment().add(2, "days");
      var result = CompletionOrLastVisit(editing, step);
      var error = result.fp17_incomplete_treatment.completion_or_last_visit;
      expect(error).toEqual("Date of acceptance cannot be in the future");
    });

    it('should not error if there is not error if completion or last visit is today', function(){
      editing.fp17_incomplete_treatment.completion_or_last_visit = moment();
      var result = CompletionOrLastVisit(editing, step);
      expect(result).toBeUndefined();
    });
  });

  describe('completion or last visit must be equal or greater than the date of acceptance', function(){
    it('should error if acceptance is after completion or last visit', function(){
      editing.fp17_incomplete_treatment.completion_or_last_visit = day1;
      editing.fp17_incomplete_treatment.date_of_acceptance = day2;
      var result = CompletionOrLastVisit(editing, step);
      var err = "Completion or last visit must be greater than the day of acceptance"
      var result = CompletionOrLastVisit(editing, step);
      var error = result.fp17_incomplete_treatment.completion_or_last_visit;
      expect(error).toEqual(err);
    });

    it('should not error acceptance is the same as completion', function(){
      editing.fp17_incomplete_treatment.completion_or_last_visit =day1;
      editing.fp17_incomplete_treatment.date_of_acceptance = day1;
      var result = CompletionOrLastVisit(editing, step);
      expect(result).toBeUndefined();
    });
  });

  describe('if there is a concurrent episode it should error', function(){
    it('should error if there is a concurrent surrounding episode', function(){
      step.overlapping_dates = [[day2, day3]];
      editing.fp17_incomplete_treatment.date_of_acceptance = day1;
      editing.fp17_incomplete_treatment.completion_or_last_visit =day2;
      var result = CompletionOrLastVisit(editing, step);
      var error = result.fp17_incomplete_treatment.date_of_acceptance;
      expect(error).toBe("The FP17 overlaps with another FP17 of this patient");
    });

    it('should not error if it is urgent treatment', function(){
      step.overlapping_dates = [[day2, day3]];
      editing.fp17_incomplete_treatment.date_of_acceptance = day1;
      editing.fp17_incomplete_treatment.completion_or_last_visit =day2;
      editing.fp17_treatment_category.treatment_category = URGENT_TREATMENT;
      var result = CompletionOrLastVisit(editing, step);
      expect(result).toBeUndefined()
    });

    it('should not error if it is denture repairs', function(){
      step.overlapping_dates = [[day2, day3]];
      editing.fp17_incomplete_treatment.date_of_acceptance = day1;
      editing.fp17_incomplete_treatment.completion_or_last_visit =day2;
      editing.fp17_treatment_category.treatment_category = DENTURE_REPAIRS;
      var result = CompletionOrLastVisit(editing, step);
      expect(result).toBeUndefined()
    });

    it('should not error if it is bridge repairs', function(){
      step.overlapping_dates = [[day2, day3]];
      editing.fp17_incomplete_treatment.date_of_acceptance = day1;
      editing.fp17_incomplete_treatment.completion_or_last_visit =day2;
      editing.fp17_treatment_category.treatment_category = BRIDGE_REPAIRS;
      var result = CompletionOrLastVisit(editing, step);
      expect(result).toBeUndefined();
    });

    it('should not error if the concurrent episode does not overlap', function(){
      step.overlapping_dates = [[day1, day2]];
      editing.fp17_incomplete_treatment.date_of_acceptance = day3;
      editing.fp17_incomplete_treatment.completion_or_last_visit = day3;
      var result = CompletionOrLastVisit(editing, step);
      expect(result).toBeUndefined();
    });
  });
});
