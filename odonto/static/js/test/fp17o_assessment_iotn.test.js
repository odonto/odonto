describe('FP17OAssessmentIOTN', function() {
  "use strict";
  var FP17OAssessmentIOTN;
  var editing;

  beforeEach(module('opal.filters'));
  beforeEach(module('opal.services'));

  beforeEach(function(){
      inject(function($injector){
        FP17OAssessmentIOTN  = $injector.get('FP17OAssessmentIOTN');
      });
      editing = {
        orthodontic_assessment: {
          iotn: undefined,
          assessment: undefined
        },
      };
  });

  describe('Other assessment types require any IOTN value', function(){
    it('should not error if assessment is set but not completed and IOTN is 1-5', function(){
      editing.orthodontic_assessment.iotn = "1";
      editing.orthodontic_assessment.assessment = "Assessment & review";
      expect(FP17OAssessmentIOTN(editing)).toBe(undefined);
    });

    it('should not error if assessment is set but not completed and IOTN is N/A', function(){
      editing.orthodontic_assessment.iotn = "N/A";
      editing.orthodontic_assessment.assessment = "Assessment & review";
      expect(FP17OAssessmentIOTN(editing)).toBe(undefined);
    });

    it('should error if assessment is set but not completed and IOTN is not set', function(){
      editing.orthodontic_assessment.assessment = "Assessment & review";
      var expected = {
        orthodontic_assessment: {iotn: "'Assessment & review' requires an IOTN"}
      }
      expect(FP17OAssessmentIOTN(editing)).toEqual(expected);
    });
  });

  describe('Assess & appliance fitted requires an IOTN of 1-5', function(){
    it('should not error if assessment is tAssess & appliance fitted and IOTN is 1', function(){
      editing.orthodontic_assessment.iotn = "1";
      editing.orthodontic_assessment.assessment = "Assess & appliance fitted";
      expect(FP17OAssessmentIOTN(editing)).toBe(undefined);
    });

    it('should error if assessment is assess & appliance fitted and IOTN is not set', function(){
      editing.orthodontic_assessment.assessment = "Assess & appliance fitted";
      var expected = {
        orthodontic_assessment: {iotn: "'Assess & appliance fitted' requires an IOTN of 1-5"}
      }
      expect(FP17OAssessmentIOTN(editing)).toEqual(expected);
    });

    it('should error if assessment is assess & appliance fitted and IOTN is N/A', function(){
      editing.orthodontic_assessment.iotn = "N/A";
      editing.orthodontic_assessment.assessment = "Assess & appliance fitted";
      var expected = {
        orthodontic_assessment: {iotn: "'Assess & appliance fitted' requires an IOTN of 1-5"}
      }
      expect(FP17OAssessmentIOTN(editing)).toEqual(expected);
    });
  });
});
