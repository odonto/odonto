describe('Fp17OTreatmentType', function() {
  "use strict";
  var Fp17OProposedTreatment;
  var editing, inCorrectError;

  beforeEach(module('opal.services'));

  beforeEach(function(){
      inject(function($injector){
        Fp17OProposedTreatment  = $injector.get('Fp17OProposedTreatment');
      });
      editing = {
        orthodontic_assessment: {},
        orthodontic_data_set: {},
      };

      inCorrectError = {
        orthodontic_assessment: {
          assessment: "Treatment type 'Proposed' is required when assessment is 'Assess & appliance fitted'"
        }
      }
  });

  it('should error if we have assess and appliance fitted and not proposed ', function(){
    editing.orthodontic_assessment.assessment = "Assess & appliance fitted";
    expect(Fp17OProposedTreatment(editing)).toEqual(inCorrectError);
  });

  it('should not error if we assessment is not assess and appliance fitted', function(){
    editing.orthodontic_assessment.assessment = "Assessment & review";
    expect(Fp17OProposedTreatment(editing)).toBe(undefined);
  });

  it('should not error if the treatment is proposed', function(){
    editing.orthodontic_assessment.assessment = "Assess & appliance fitted";
    editing.orthodontic_data_set.treatment_type = "Proposed";
    expect(Fp17OProposedTreatment(editing)).toBe(undefined);
  });
});