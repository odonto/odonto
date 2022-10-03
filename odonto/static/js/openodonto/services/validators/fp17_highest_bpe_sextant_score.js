angular.module('opal.services').factory('Fp17HighestBpeSextantScore', function(ValidatorUtils){
  /*
	*  England now want to record BPE as a mandatory item on adult banded
	*  claims but they only require the highest sextant score in the mouth.
	*
	*  This code is mandatory on all adult banded claims (Bands 1, 2 and 3)
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

		if(!editing.fp17_clinical_data_set.highest_bpe_score){
			return {
				fp17_clinical_data_set: {
					highest_bpe_score: "Adult bands 1, 2 and 3 require a highest BPE score"
				}
			}
		}
  }
});
