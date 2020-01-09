describe('AssessmentIOTN', function() {
  "use strict";
  var AssessmentIOTN;
  var editing;

  beforeEach(module('opal.filters'));
  beforeEach(module('opal.services'));

  beforeEach(function(){
      inject(function($injector){
        AssessmentIOTN  = $injector.get('AssessmentIOTN');
      });
      editing = {
        orthodontic_assessment: {
          iotn: undefined,
          iotn_not_applicable: undefined
        }
      };
  });

  it('should not error if only IOTN is set', function(){
    editing.orthodontic_assessment.iotn = 1;
    expect(AssessmentIOTN(editing)).toBe(undefined);
  });

  it('should not error if only IOTN not applicable is set', function(){
    editing.orthodontic_assessment.iotn_not_applicable = true;
    expect(AssessmentIOTN(editing)).toBe(undefined);
  });

  it('should error if both IOTN and IOTN not applicable are set', function(){
    editing.orthodontic_assessment.iotn = 1;
    editing.orthodontic_assessment.iotn_not_applicable = true;
    var expected = {
      orthodontic_assessment: {iotn_not_applicable: "There cannot be both IOTN and IOTN not applicable"}
    }
    expect(AssessmentIOTN(editing)).toEqual(expected);
  });
});
