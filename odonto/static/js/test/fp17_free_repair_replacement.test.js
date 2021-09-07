describe('Fp17FreeRepaireReplacement', function() {
  "use strict";
	var editing, Fp17FreeRepaireReplacement;

  beforeEach(module('opal.services'));

  beforeEach(function(){
      editing = {
				fp17_other_dental_services: {
					free_repair_or_replacement: false
				},
				fp17_clinical_data_set: {
					referral_for_advanced_mandatory_services_band: null
				}
			};

			inject(function($injector){
        Fp17FreeRepaireReplacement  = $injector.get('Fp17FreeRepaireReplacement');
      })
  });

	it('should error if there is both a free_repair_or_replacement and referral_for_advanced_mandatory_services_band', function(){
		editing.fp17_other_dental_services.free_repair_or_replacement = true;
		editing.fp17_clinical_data_set.referral_for_advanced_mandatory_services_band = 1;
		var err = {
			fp17_other_dental_services: {
				free_repair_or_replacement: "A free repair is not allowed with a referral for AMS"
			}
		};
		expect(Fp17FreeRepaireReplacement(editing)).toEqual(err);
	});

	it('should not error if there is no free_repair_or_replacement', function(){
		editing.fp17_other_dental_services.free_repair_or_replacement = false;
		editing.fp17_clinical_data_set.referral_for_advanced_mandatory_services_band = 1;
		expect(Fp17FreeRepaireReplacement(editing)).toBe(undefined);
	});

	it('should not error if there is no referral_for_advanced_mandatory_services_band', function(){
		editing.fp17_other_dental_services.free_repair_or_replacement = true;
		editing.fp17_clinical_data_set.referral_for_advanced_mandatory_services_band = null;
		expect(Fp17FreeRepaireReplacement(editing)).toBe(undefined);
	});
});
