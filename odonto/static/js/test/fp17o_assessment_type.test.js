describe('Fp17OAssessmentType', function() {
  "use strict";
  var Fp17OAssessmentType;
  var editing, step;

  beforeEach(module('opal.filters'));
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
        }
      };
      step = {
        other_assessments: []
      }
  });

  describe('assessment is required if there is a date of referral', function(){
    it('should error if there is a date of referral but no assessment', function(){
      editing.orthodontic_assessment.date_of_referral = new Date();
      var expected = {
        "orthodontic_assessment": {
          "assessment": "An assessment type is required when there is a date of referral"
        }
      }
      expect(Fp17OAssessmentType(editing, step)).toEqual(expected);
    });

    it('should error if there is a date of referral but assessment is null', function(){
      editing.orthodontic_assessment.date_of_referral = new Date();
      editing.orthodontic_assessment.assessment = null;
      var expected = {
        "orthodontic_assessment": {
          "assessment": "An assessment type is required when there is a date of referral"
        }
      }
      expect(Fp17OAssessmentType(editing, step)).toEqual(expected);
    });

    it('should not error if there is no date of referral', function(){
      expect(Fp17OAssessmentType(editing, step)).toBe(undefined);
    });

    it('should not error if there is a date of referral and an assessment', function(){
      editing.orthodontic_assessment.date_of_referral = new Date();
      editing.orthodontic_assessment.assessment = "Assessment & Review"
      expect(Fp17OAssessmentType(editing, step)).toBe(undefined);
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
      expect(Fp17OAssessmentType(editing, step)).toEqual(expected);
    });

    it('should not error if there is an assessment', function(){
      editing.orthodontic_assessment.assessment = "Assessment & Review";
      editing.orthodontic_treatment.completion_type = "";
      expect(Fp17OAssessmentType(editing, step)).toBe(undefined);
    });

    it('it should not error if there is a completion type', function(){
      expect(Fp17OAssessmentType(editing, step)).toBe(undefined);
    });

    it('should not error if there is a repair', function(){
      editing.orthodontic_treatment.completion_type = "";
      editing.orthodontic_treatment.repair = true;
      expect(Fp17OAssessmentType(editing, step)).toBe(undefined);
    });

    it('should not error if there is a regulation', function(){
      editing.orthodontic_treatment.completion_type = "";
      editing.orthodontic_treatment.replacement = true;
      expect(Fp17OAssessmentType(editing, step)).toBe(undefined);
    });
  });

  describe('after an assessment and appliance fitted, the next fp17o for the patient cannot be another assessment', function(){
    it('should error if there is a previous claim and it is an assessment', function(){
      step.other_assessments = [{
        date: '20/08/2021',
        assessment: 'Assess & appliance fitted'
      }];
      editing.orthodontic_treatment.completion_type = '';
      editing.orthodontic_assessment.date_of_referral = new Date();
      editing.orthodontic_assessment.date_of_assessment = new Date();
      editing.orthodontic_assessment.assessment = 'Assess & appliance fitted';
      var error = {
        orthodontic_assessment: {
          assessment: "This cannot have an assessment type as the patient's previous FP17O was 'Assess & appliance fitted'"
        }
      }
      expect(Fp17OAssessmentType(editing, step)).toEqual(error);
    });

    it('should not error if it is not an assessment', function(){
      expect(Fp17OAssessmentType(editing, step)).toBe(undefined);
    });

    it('should not error if there are no previous submitted claims', function(){
      editing.orthodontic_treatment.completion_type = '';
      editing.orthodontic_assessment.date_of_referral = new Date();
      editing.orthodontic_assessment.date_of_assessment = new Date();
      editing.orthodontic_assessment.assessment = 'Assess & appliance fitted'
      expect(Fp17OAssessmentType(editing, step)).toBe(undefined);
    });

    it('should not error if there is a previous assessment but there is another claim between', function(){
      step.other_assessments = [
        {
          date: '20/08/2021',
          assessment: 'Assess & appliance fitted'
        },
        {
          date: '21/08/2021',
          assessment: null
        }
      ];
      editing.orthodontic_treatment.completion_type = '';
      editing.orthodontic_assessment.date_of_referral = new Date();
      editing.orthodontic_assessment.date_of_assessment = new Date();
      editing.orthodontic_assessment.assessment = 'Assess & appliance fitted';
      expect(Fp17OAssessmentType(editing, step)).toBe(undefined);
    });

    it('should not error if there is an assessment but its in the future', function(){
      var today = new Date();
      var future = new Date();
      future.setFullYear(today.getFullYear() + 1);
      step.other_assessments = [{
        date: future,
        assessment: 'Assess & appliance fitted'
      }];
      editing.orthodontic_treatment.completion_type = '';
      editing.orthodontic_assessment.date_of_referral = today;
      editing.orthodontic_assessment.date_of_assessment = today;
      editing.orthodontic_assessment.assessment = 'Assess & appliance fitted';
      var error = {
        orthodontic_assessment: {
          assessment: "This cannot have an assessment type as the patient's previous FP17O was 'Assess & appliance fitted'"
        }
      }
      expect(Fp17OAssessmentType(editing, step)).toBe(undefined);
    });

  });
});
