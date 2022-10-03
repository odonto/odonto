angular.module('opal.services').factory('Fp17UntreatedDecayedTeeth', function(ValidatorUtils){
	/*
	* According to CHANGE CONTROL NOTE 50
	* Untreated decayed Teeth is mandatory on all adult banded claims (Bands 1, 2 and 3)
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

		if(!editing.fp17_clinical_data_set.untreated_decayed_teeth && editing.fp17_clinical_data_set.untreated_decayed_teeth !== 0){
			return {
				fp17_clinical_data_set: {
					untreated_decayed_teeth: "Adult bands 1, 2 and 3 require an entry of untreated decayed teeth"
				}
			}
		}
  }
});
