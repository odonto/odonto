angular.module('opal.services').factory('Fp17NumberOfMonths', function(ValidatorUtils){
	/*
	* According to CHANGE CONTROL NOTE 50
	* This existing recall interval code 9172 is to be made
	* mandatory on all adult English banded claims (Bands 1, 2 and 3)
	*
	* Note this is only true for over 18s and those not from overseas
	*/
  return function(editing){
		var dateOfAcceptance = editing.fp17_incomplete_treatment.date_of_acceptance;
		if(!ValidatorUtils.eighteen_or_over(editing, dateOfAcceptance)){
			return;
		}

		var treatmentCategory = editing.fp17_treatment_category.treatment_category;
		if(!treatmentCategory){
			return;
		}

		var bands = ["Band 1", "Band 2", "Band 3"];
		if(bands.indexOf(treatmentCategory) === -1){
			return;
		}

		if(!editing.fp17_recall.number_of_months && editing.fp17_recall.number_of_months !== 0){
			return {
				fp17_recall: {
					number_of_months: "Adult bands 1, 2 and 3 require a recall interval"
				}
			}
		}
  }
});
