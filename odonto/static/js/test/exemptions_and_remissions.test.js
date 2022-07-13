describe('ExemptionsAndRemissionsValidator', function() {
  "use strict";
  var ExemptionsAndRemissionsValidator;
  var editing;
  var noExemptionOrChargeError = {
    fp17_exemptions: {
      step_error: "Please select an exemption or add the charge"
    }
  }

  var partialError = {
    fp17_exemptions: {
      step_error: "A charge is required if there is only a partial exemption"
    }
  }

  beforeEach(module('opal.services'));

  beforeEach(function(){
      inject(function($injector){
        ExemptionsAndRemissionsValidator  = $injector.get('ExemptionsAndRemissionsValidator');
      });
      editing = {
        fp17_exemptions: {},
        fp17_other_dental_services: {},
      };

  });

  it('should error if there is no exemption charge or free repair', function(){
    expect(ExemptionsAndRemissionsValidator(editing)).toEqual(noExemptionOrChargeError);
  });

  it('should show a different error if there is a partial exemption', function(){
    editing.fp17_exemptions.partial_remission_hc3_cert = true
    expect(ExemptionsAndRemissionsValidator(editing)).toEqual(partialError);
  });

  it('should not error if there is an exemption', function(){
    editing.fp17_exemptions.patient_under_18 = true;
    expect(ExemptionsAndRemissionsValidator(editing)).toBeUndefined();
  });

  it('should not error if there is a charge', function(){
    editing.fp17_exemptions.patient_charge_collected = 10;
    expect(ExemptionsAndRemissionsValidator(editing)).toBeUndefined();
  });

  it('should not error if there is a free reppair', function(){
    editing.fp17_other_dental_services.free_repair_or_replacement = true;
    expect(ExemptionsAndRemissionsValidator(editing)).toBeUndefined();
  });
});
