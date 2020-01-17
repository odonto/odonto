describe('Fp17OAssessmentAestheticComponent', function() {
  "use strict";
  var Fp17OAssessmentAestheticComponent;
  var editing;

  beforeEach(module('opal.services'));

  beforeEach(function(){
    inject(function($injector){
      Fp17OAssessmentAestheticComponent  = $injector.get('Fp17OAssessmentAestheticComponent');
    });
    editing = {
      orthodontic_assessment: {
        iotn: undefined,
        aesthetic_component: undefined
      }
    }
  });

  it('should error if IOTN is 3 and aesthetic component is not set', function(){
    var expected = {
      orthodontic_assessment: {aesthetic_component: "IOTN 3 requires an aesthetic component"}
    };
    editing.orthodontic_assessment.iotn = "3";
    expect(Fp17OAssessmentAestheticComponent(editing)).toEqual(expected);
  });

  it('should not error if IOTN is 3 and aesthetic component is set', function(){
    editing.orthodontic_assessment.iotn = "3";
    editing.orthodontic_assessment.aesthetic_component = 2;
    expect(Fp17OAssessmentAestheticComponent(editing)).toBe(undefined);
  });

  it('should not error if IOTN is not 3', function(){
    editing.orthodontic_assessment.iotn = "2";
    expect(Fp17OAssessmentAestheticComponent(editing)).toBe(undefined);
  });
});