describe('Fp17ORegulation11', function() {
  "use strict";
  var Fp17ORegulation11;
  var editing;

  beforeEach(module('opal.services'));

  beforeEach(function(){
      inject(function($injector){
        Fp17ORegulation11  = $injector.get('Fp17ORegulation11');
      });
      editing = {
        orthodontic_treatment: {
					replacement: false
				},
				fp17_exemptions: {
					patient_charge_collected: null
				}
      };
  });

	it('Should not error if there is a patient charge', function(){
		editing.orthodontic_treatment.replacement = true;
		editing.fp17_exemptions.patient_charge_collected = 2;
		expect(Fp17ORegulation11(editing)).toBe(undefined);
	});

	it('Should not error if it is not reg 11', function(){
		editing.orthodontic_treatment.replacement = false;
		editing.fp17_exemptions.patient_charge_collected = undefined;
		expect(Fp17ORegulation11(editing)).toBe(undefined);
	})

	it('Should error if it is reg 11 and there is no patient charge', function(){
		editing.orthodontic_treatment.replacement = true;
		editing.fp17_exemptions.patient_charge_collected = undefined;
		var err = {
			orthodontic_treatment: {
				replacement: "Reg 11 requires a patient charge"
			}
		}
		expect(Fp17ORegulation11(editing)).toEqual(err);
	})
});
