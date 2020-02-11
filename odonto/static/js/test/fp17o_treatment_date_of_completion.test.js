describe('Fp17ODateOfCompletion', function() {
  "use strict";
  var Fp17ODateOfCompletion;
  var editing;
  var step;

  beforeEach(module('opal.filters'));
  beforeEach(module('opal.services'));


  beforeEach(function(){
    inject(function($injector){
      Fp17ODateOfCompletion  = $injector.get('Fp17ODateOfCompletion');
    });
    editing = {
      orthodontic_treatment: {},
      orthodontic_assessment: {}
    };
    step = {
      overlapping_dates: []
    }
  });

  describe('if there is a completion type, date of completion is required', function(){
    it('should error if there is a completion type and no date of completion', function(){
      editing.orthodontic_treatment.completion_type = "Treatment completed";
      var result = Fp17ODateOfCompletion(editing, step);
      var error = result.orthodontic_treatment.date_of_completion;
      var msg = "Date of completion or last visit is required when there is a completion type, repair or reg 11";
      expect(error).toBe(msg);
    });

    it('should not error if there is an completion type and no date of completion', function(){
      editing.orthodontic_treatment.completion_type = "Treatment completed";
      editing.orthodontic_treatment.date_of_completion = moment('2019-04-05').toDate();
      var result = Fp17ODateOfCompletion(editing, step);
      expect(result).toBeUndefined();
    });

    it('should not error if there is a reg 11 and no date of completion', function(){
      editing.orthodontic_treatment.replacement = true;
      editing.orthodontic_treatment.date_of_completion = moment('2019-04-05').toDate();
      var result = Fp17ODateOfCompletion(editing, step);
      expect(result).toBeUndefined();
    });

    it('should not error if there is a repair and no date of completion', function(){
      editing.orthodontic_treatment.repair = true;
      editing.orthodontic_treatment.date_of_completion = moment('2019-04-05').toDate();
      var result = Fp17ODateOfCompletion(editing, step);
      expect(result).toBeUndefined();
    });
  });

  describe('date of completion cannot be in the future', function(){
    it('should error if the date of completion type is not in the future', function(){
      editing.orthodontic_treatment.completion_type = "Treatment completed";
      editing.orthodontic_treatment.date_of_completion = moment().add(2, "d").toDate();
      var result = Fp17ODateOfCompletion(editing, step);
      var error = result.orthodontic_treatment.date_of_completion;
      expect(error).toBe("Date of completion or last visit cannot be in the future");
    });

    it('should not error if there is no date of completion', function(){
      var result = Fp17ODateOfCompletion(editing, step);
      expect(result).toBeUndefined();
    });
  });

  describe('date of completion cannot overlap with other episodes', function(){
    var day1 = moment().subtract(3, "days");
    var day2 = moment().subtract(2, "days");
    var day3 = moment().subtract(1, "days");
    var day4 = moment();

    it('should error if another episode is between assessment and completion', function(){
      editing.orthodontic_assessment.date_of_assessment = day1;
      editing.orthodontic_treatment.date_of_completion = day3;
      step.overlapping_dates = [{dates: [day2]}];
      var result = Fp17ODateOfCompletion(editing, step);
      var error = result.orthodontic_treatment.date_of_completion;
      expect(error).toBe("The FP17O overlaps with another FP17O of this patient");
    });

    it('should error if another episode is between appliance fitted and completion', function(){
      editing.orthodontic_assessment.date_of_appliance_fitted = day1;
      editing.orthodontic_treatment.date_of_completion = day3;
      step.overlapping_dates = [{dates: [day2]}];
      var result = Fp17ODateOfCompletion(editing, step);
      var error = result.orthodontic_treatment.date_of_completion;
      expect(error).toBe("The FP17O overlaps with another FP17O of this patient");
    });

    it('should error if completion is within the date range of another episode', function(){
      editing.orthodontic_treatment.date_of_completion = day2;
      step.overlapping_dates = [{dates: [day1, day3]}];
      var result = Fp17ODateOfCompletion(editing, step);
      var error = result.orthodontic_treatment.date_of_completion;
      expect(error).toBe("The FP17O overlaps with another FP17O of this patient");
    });

    it('should not error if the range is not in another date range', function(){
      editing.orthodontic_assessment.date_of_appliance_fitted = day1
      editing.orthodontic_treatment.date_of_completion = day2;
      step.overlapping_dates = [{dates: [day3, day4]}];
      var result = Fp17ODateOfCompletion(editing, step);
      expect(result).toBeUndefined();
    });

    it('should not error if the date is not in another date range', function(){
      editing.orthodontic_treatment.date_of_completion = day1;
      step.overlapping_dates = [{dates: [day2, day3]}]
      var result = Fp17ODateOfCompletion(editing, step);
      expect(result).toBeUndefined();
    });
  })
});