angular.module('opal.services').factory('Fp17ORegulation11', function(){
  "use strict";
	/*
	* Regulation 11, which means that the patient has lost/broken their appliance
	* when a patient is reg 11, they always have to pay regardless of their
	* exemption.
	*/
	return function(editing){
		if(!editing.orthodontic_treatment.replacement){
			return
		}
		if(editing.fp17_exemptions.patient_charge_collected){
			return
		}
		return {
			orthodontic_treatment: {
				replacement: "Reg 11 requires a patient charge"
			}
		}
	}
});
