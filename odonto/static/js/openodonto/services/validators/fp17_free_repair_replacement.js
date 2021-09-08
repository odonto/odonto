angular.module('opal.services').factory('Fp17FreeRepaireReplacement', function(){
  "use strict";
	/*
	* If there is a free repair replacement and a referral for
	* advanced mandatory services, compass will throw an error.
	*
	* This is undocumented and although they admit its logically possible
	* they have had this check in since 2014.
	*
	* Compass state...
	* If you have a claim with Free Repair/Replacement and Referral for AMS then that claim is effectively saying:
	*   - I’ve already provided treatment for which the patient has paid but I’m replacing the item I’ve provided for free.
  *   - I’m also referring the patient on to another practice:
  * If it’s being referred for the replacement treatment then the dentist making the claim is not actually providing the free repair/replacement.
  * If it’s being referred for extra treatment then the course of treatment does not solely consist of a free repair/replacement.
	*/
	return function(editing){
		if(editing.fp17_other_dental_services.free_repair_or_replacement){
			if(editing.fp17_clinical_data_set.referral_for_advanced_mandatory_services_band){
				return {
					fp17_other_dental_services: {
						free_repair_or_replacement: "A free repair is not allowed with a referral for AMS"
					}
				}
			}
		}
	}

});
