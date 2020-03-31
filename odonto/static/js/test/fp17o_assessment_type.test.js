describe('Fp17OAssessmentType', function() {
  "use strict";
  var Fp17OAssessmentType;
  var editing;

  beforeEach(module('opal.services'));

  beforeEach(function(){
      inject(function($injector){
        Fp17OAssessmentType  = $injector.get('Fp17OAssessmentType');
      });
      editing = {
        orthodontic_assessment: {
          date_of_referral: undefined,
          assessment: ""
        },
        orthodontic_treatment: {
          completion_type: "Treatment completed"
        },
        orthodontic_data_set: {}
      };
  });

  describe('assessment is required if there is a date of referral', function(){
    it('should error if there is a date of referral but no assessment', function(){
      editing.orthodontic_assessment.date_of_referral = new Date();
      var expected = {
        "orthodontic_assessment": {
          "assessment": "An assessment type is required when there is a date of referral"
        }
      }
      expect(Fp17OAssessmentType(editing)).toEqual(expected);
    });

    it('should error if there is a date of referral but assessment is null', function(){
      editing.orthodontic_assessment.date_of_referral = new Date();
      editing.orthodontic_assessment.assessment = null;
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

  describe('either an assessment or a completion type are required', function(){
    it('should error if there is no assessment or completion_type', function(){
      var expected = {
        "orthodontic_assessment": {
          "assessment": "An assessment type, completion type, repair or reg 11 are required"
        },
        "orthodontic_treatment": {
          "completion_type": "An assessment type, completion type, repair or reg 11 are required",
          "repair": "An assessment type, completion type, repair or reg 11 are required",
          "replacement": "An assessment type, completion type, repair or reg 11 are required"
        },
      }
      editing.orthodontic_treatment.completion_type = "";
      expect(Fp17OAssessmentType(editing)).toEqual(expected);
    });

    it('should not error if there is an assessment', function(){
      editing.orthodontic_assessment.assessment = "Assessment & Review";
      editing.orthodontic_treatment.completion_type = "";
      expect(Fp17OAssessmentType(editing)).toBe(undefined);
    });

    it('it should not error if there is a completion type', function(){
      expect(Fp17OAssessmentType(editing)).toBe(undefined);
    });

    it('should not error if there is a repair', function(){
      editing.orthodontic_treatment.completion_type = "";
      editing.orthodontic_treatment.repair = true;
      expect(Fp17OAssessmentType(editing)).toBe(undefined);
    });

    it('should not error if there is a regulation', function(){
      editing.orthodontic_treatment.completion_type = "";
      editing.orthodontic_treatment.replacement = true;
      expect(Fp17OAssessmentType(editing)).toBe(undefined);
    });
  });

  describe('treatment type is proposed but assessment type is not assess and appliance', function(){
    it('should error if assessment is not assess and appliance fitted but treatment type is proposed', function(){
      editing.orthodontic_data_set.treatment_type = "Proposed"
      editing.orthodontic_assessment.assessment = "Assessment & Review";
      expect(Fp17OAssessmentType(editing)).toEqual({
        orthodontic_assessment: {
          assessment: "Treatment type 'Proposed' is required when assessment is 'Assess & appliance fitted'"
        }
      });
    });

    it('should not error if assessment type is assess and appliance fitted and treatment is proposed', function(){
      editing.orthodontic_data_set.treatment_type = "Proposed"
      editing.orthodontic_assessment.assessment = "Assess & appliance fitted";
      expect(Fp17OAssessmentType(editing)).toBe(undefined);
    })

    it('should not error if assessment is not proposed', function(){
      editing.orthodontic_data_set.treatment_type = undefined;
      editing.orthodontic_assessment.assessment = "Assessment & Review";
      expect(Fp17OAssessmentType(editing)).toBe(undefined);
    });
  });
});