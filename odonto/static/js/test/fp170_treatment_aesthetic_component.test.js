describe('Fp17OTreatmentAestheticComponent', function() {
  "use strict";
  var Fp17OTreatmentAestheticComponent;
  var editing;

  beforeEach(module('opal.services'));

  beforeEach(function(){
    inject(function($injector){
      Fp17OTreatmentAestheticComponent  = $injector.get('Fp17OTreatmentAestheticComponent');
    });
    editing = {
      orthodontic_treatment: {
        iotn: undefined,
        aesthetic_component: undefined
      }
    }
  });

  it('should error if IOTN is 3 and aesthetic component is not set', function(){
    var expected = {
      orthodontic_treatment: {aesthetic_component: "IOTN 3 requires an aesthetic component"}
    };
    editing.orthodontic_treatment.iotn = "3";
    expect(Fp17OTreatmentAestheticComponent(editing)).toEqual(expected);
  });

  it('should not error if IOTN is 3 and aesthetic component is set', function(){
    editing.orthodontic_treatment.iotn = "3";
    editing.orthodontic_treatment.aesthetic_component = 2;
    expect(Fp17OTreatmentAestheticComponent(editing)).toBe(undefined);
  });

  it('should not error if IOTN is not 3', function(){
    editing.orthodontic_treatment.iotn = "2";
    expect(Fp17OTreatmentAestheticComponent(editing)).toBe(undefined);
  });
});