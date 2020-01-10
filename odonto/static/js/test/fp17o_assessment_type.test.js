describe('Fp17OAssessmentType', function() {
  "use strict";
  var Fp17OAssessmentType;
  var editing;

  beforeEach(module('opal.services'));

  beforeEach(function(){
      inject(function($injector){
        Fp17OAssessmentType  = $injector.get('Fp17OAssessmentType');
      });
      editing = {orthodontic_assessment: {
        date_of_referral: undefined,
        assessment: ""
      }};
  });

  it('should error if there is a date of referral but no assessment', function(){
    editing.orthodontic_assessment.date_of_referral = new Date();
    var expected = {
      "orthodontic_assessment": {
        "assessment": "An assessment type is required when there is a date of referral"
      }
    }
    expect(Fp17OAssessmentType(editing)).toEqual(expected);
  });

  it('should not error if there is no date of referral', function(){
    expect(Fp17OAssessmentType(editing)).toBe(undefined);
  });

  it('should not error if there is a date of referral and an assessment', function(){
    editing.orthodontic_assessment.date_of_referral = new Date();
    editing.orthodontic_assessment.assessment = "Assessment & Review"
    expect(Fp17OAssessmentType(editing)).toBe(undefined);
  });

});