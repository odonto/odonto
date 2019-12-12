describe('Fp17ODateOfAssessment', function() {
  "use strict";
  var Fp17ODateOfAssessment;
  var editing;

  beforeEach(module('opal.filters'));
  beforeEach(module('opal.services'));


  beforeEach(function(){
    inject(function($injector){
      Fp17ODateOfAssessment  = $injector.get('Fp17ODateOfAssessment');
    });
    editing = {
      orthodontic_assessment: {}
    };
  });

  describe('if there is an assessment type date of assessment is required', function(){
    it('should error if there is an assessment type and no date of assessment', function(){
      editing.orthodontic_assessment.assessment = "Assessment & Review";
      var result = Fp17ODateOfAssessment(editing);
      var error = result.orthodontic_assessment.date_of_assessment;
      expect(error).toBe("Date of assessment is required when there is an assessment type");
    });

    it('should not error if there is an assessment type and no date of assessment', function(){
      editing.orthodontic_assessment.assessment = "Assessment & Review";
      editing.orthodontic_assessment.date_of_assessment = moment('2019-04-05').toDate();
      var result = Fp17ODateOfAssessment(editing);
      expect(result).toBeUndefined();
    });
  });

  describe('date of assessment cannot be in the future', function(){
    it('should error if the date of assessment is not in the future', function(){
      editing.orthodontic_assessment.assessment = "Assessment & Review";
      editing.orthodontic_assessment.date_of_assessment = moment().add(2, "d").toDate();
      var result = Fp17ODateOfAssessment(editing);
      var error = result.orthodontic_assessment.date_of_assessment;
      expect(error).toBe("Date of assessment cannot be in the future");
    });

    it('should not error if there is no date of assessment', function(){
      var result = Fp17ODateOfAssessment(editing);
      expect(result).toBeUndefined();
    });
  });
});