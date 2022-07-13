describe('Fp17OCompletionType', function() {
  "use strict";
  var editing, step;
  var Fp17OCompletionType;

  beforeEach(module('opal.filters'));
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
      },
      orthodontic_data_set: {}
    };
    step = {
      overlapping_dates: []
    }
  });

  describe('completion type and assess and refuse treatment', function(){
    it('should error if there is a completion type and an assessment of Assess & refuse treatment', function(){
      editing.orthodontic_assessment.assessment = "Assess & refuse treatment";
      editing.orthodontic_treatment.completion_type = "Treatment completed";
      var expected = {
        orthodontic_treatment: {
          completion_type: 'There cannot be a completion type and an assessment type of "Assess & refuse treatment"'
        }
      }
      expect(Fp17OCompletionType(editing, step)).toEqual(expected);
    });

    it('should not error if there is a completion type and an assessment of something other than Assess & refuse treatment', function(){
      editing.orthodontic_assessment.assessment = "Assessment & review";
      editing.orthodontic_treatment.completion_type = "Treatment completed";
      expect(Fp17OCompletionType(editing, step)).toBe(undefined);
    });

    it('should not error if there is a completion type and no assessment type', function(){
      editing.orthodontic_assessment.assessment = null;
      editing.orthodontic_treatment.completion_type = "Treatment completed";
      expect(Fp17OCompletionType(editing, step)).toBe(undefined);
    });

    it('shold not error if there is no completion type and an assessment of Assess & refuse treatment', function(){
      editing.orthodontic_assessment.assessment = "Assessment & review";
      editing.orthodontic_treatment.completion_type = "";
      expect(Fp17OCompletionType(editing, step)).toBe(undefined);
    });
  });

  describe('Sequential episodes cannot also be treatment completed', function(){
    var day1 = moment().subtract(3, "days");
    var day2 = moment().subtract(2, "days");
    var day3 = moment().subtract(1, "days");

    it('should not error if there is no completion type', function(){
      editing.orthodontic_assessment.assessment = null;
      editing.orthodontic_treatment.completion_type = null;
      expect(Fp17OCompletionType(editing, step)).toBe(undefined);
    });

    it('should error if the previous episode has a completion type', function(){
      step.overlapping_dates = [{
        "dates": [day1, day2],
        "completion_type": "Treatment completed"
      }]
      editing.orthodontic_treatment.completion_type = "Treatment completed";
      editing.orthodontic_treatment.date_of_completion = day3;
      var expected = {
        orthodontic_treatment: {
          completion_type: 'The previous claim was also a completion'
        }
      }
      expect(Fp17OCompletionType(editing, step)).toEqual(expected);
    });

    it('should not error if the most recent episode does not have a completion type', function(){
      step.overlapping_dates = [
        {
          "dates": [day1],
          "completion_type": "Treatment completed"
        },
        {
          "dates": [day2],
          "completion_type": undefined
        }
      ]
      editing.orthodontic_treatment.completion_type = "Treatment completed";
      editing.orthodontic_treatment.date_of_completion = day3;
      expect(Fp17OCompletionType(editing, step)).toBe(undefined);;
    });

    it('should error if the next episode has a completion type', function(){
      step.overlapping_dates = [{
        "dates": [day2, day3],
        "completion_type": "Treatment completed"
      }]
      editing.orthodontic_treatment.completion_type = "Treatment completed";
      editing.orthodontic_treatment.date_of_completion = day1;
      var expected = {
        orthodontic_treatment: {
          completion_type: 'The next claim for this patient is also a completion'
        }
      }
      expect(Fp17OCompletionType(editing, step)).toEqual(expected);
    });

    it('should not error if the subsequent episode does not have a completion type', function(){
      step.overlapping_dates = [
        {
          "dates": [day2],
          "completion_type": undefined
        },
        {
          "dates": [day3],
          "completion_type": "Treatment completed"
        }
      ]
      editing.orthodontic_treatment.completion_type = "Treatment completed";
      editing.orthodontic_treatment.date_of_completion = day1;
      expect(Fp17OCompletionType(editing, step)).toBe(undefined);;
    });


  });
});
