describe('Fp17OCompletionType', function() {
  "use strict";
  var editing;
  var Fp17OCompletionType;

  beforeEach(module('opal.services'));

  beforeEach(function(){
    inject(function($injector){
      Fp17OCompletionType  = $injector.get('Fp17OCompletionType');
    });
    editing = {
      orthodontic_assessment: {
        assessment: null
      },
      orthodontic_treatment: {
        completion_type: null
      }
    };
  });

  it('should error if there is a completion type and an assessment of Assess & refuse treatment', function(){
    editing.orthodontic_assessment.assessment = "Assess & refuse treatment";
    editing.orthodontic_treatment.completion_type = "Treatment completed";
    var expected = {
      orthodontic_treatment: {
        completion_type: 'There cannot be a completion type and an assessment type of "Assess & refuse treatment"'
      }
    }
    expect(Fp17OCompletionType(editing)).toEqual(expected);
  });

  it('should not error if there is a completion type and an assessment of something other than Assess & refuse treatment', function(){
    editing.orthodontic_assessment.assessment = "Assessment & review";
    editing.orthodontic_treatment.completion_type = "Treatment completed";
    expect(Fp17OCompletionType(editing)).toBe(undefined);
  });

  it('should not error if there is a completion type and no assessment type', function(){
    editing.orthodontic_assessment.assessment = null;
    editing.orthodontic_treatment.completion_type = "Treatment completed";
    expect(Fp17OCompletionType(editing)).toBe(undefined);
  });

  it('shold not error if there is no completion type and an assessment of Assess & refuse treatment', function(){
    editing.orthodontic_assessment.assessment = "Assessment & review";
    editing.orthodontic_treatment.completion_type = "";
    expect(Fp17OCompletionType(editing)).toBe(undefined);
  });
});