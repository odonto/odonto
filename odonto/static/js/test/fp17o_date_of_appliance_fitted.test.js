describe('Fp17ODateOfApplianceFitted', function() {
  "use strict";
  var Fp17ODateOfApplianceFitted;
  var editing, step;

  beforeEach(module('opal.filters'));
  beforeEach(module('opal.services'));


  beforeEach(function(){
    inject(function($injector){
      Fp17ODateOfApplianceFitted  = $injector.get('Fp17ODateOfApplianceFitted');
    });
    editing = {
      orthodontic_assessment: {}
    };
    step = {
      overlapping_dates: []
    }
  });

  describe('date of appliance fitted should not be in other dates of another episode', function(){
    var day1 = moment().subtract(3, "days");
    var day2 = moment().subtract(2, "days");
    var day3 = moment().subtract(1, "days");

    it('should error if the date of appliance fitted is between other dates', function(){
      step.overlapping_dates = [{dates: [day1, day3]}];
      editing.orthodontic_assessment.date_of_appliance_fitted = day2;
      var result = Fp17ODateOfApplianceFitted(editing, step);
      var error = result.orthodontic_assessment.date_of_appliance_fitted;
      expect(error).toBe("The FP17O overlaps with another FP17O of this patient");
    });

    it('should not error if the date of appliance fitted is not between other dates', function(){
      step.overlapping_dates = [{dates: [day2, day3]}];
      editing.orthodontic_assessment.date_of_appliance_fitted = day1;
      var result = Fp17ODateOfApplianceFitted(editing, step);
      expect(result).toBeUndefined();
    });

    it('should should error if the date of assessment and date of appliance fitted have a date between them', function(){
      step.overlapping_dates = [{dates: [day2]}];
      editing.orthodontic_assessment.date_of_assessment = day1;
      editing.orthodontic_assessment.date_of_appliance_fitted = day3;
      var result = Fp17ODateOfApplianceFitted(editing, step);
      var error = result.orthodontic_assessment.date_of_appliance_fitted;
      expect(error).toBe("The FP17O overlaps with another FP17O of this patient");
    });

    it('should error the date of appliance fitted is on another date', function(){
      step.overlapping_dates = [{dates: [day2]}];
      editing.orthodontic_assessment.date_of_assessment = day1;
      editing.orthodontic_assessment.date_of_appliance_fitted = day2;
      var result = Fp17ODateOfApplianceFitted(editing, step);
      var error = result.orthodontic_assessment.date_of_appliance_fitted;
      expect(error).toBe("The FP17O overlaps with another FP17O of this patient");
    });
  });
});