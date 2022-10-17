angular.module('opal.services').factory('ValidatorUtils', function(toMomentFilter){
	return {
		eighteen_or_over: function(editing, otherDate){
			/*
			* Returns
			* true if the patient is 18 or over at the time of the otherDate
			* false if the patient is not over 18
			* null if we cannot work it out
			*/
			if(!editing.demographics.date_of_birth || !otherDate){
				return null;
			}
			// we wrap it in a moment as moments are changed in place by add
			var dobMoment = moment(toMomentFilter(editing.demographics.date_of_birth));
			var otherMoment = toMomentFilter(otherDate);
			var eighteenBirthday = dobMoment.add(18, 'years');
			var overEighteen = otherMoment.diff(eighteenBirthday, "days") >= 0;
			return overEighteen;
		},
		hasExemption: function(editing){
			/*
			* Returns true if a patient has any exemptions
			* note his returns false for partial remissions
			*/
			var EXEMPTION_FIELDS = [
				"patient_under_18",
				"full_remission_hc2_cert",
				"expectant_mother",
				"nursing_mother",
				"aged_18_in_full_time_education",
				"income_support",
				"nhs_tax_credit_exemption",
				"income_based_jobseekers_allowance",
				"pension_credit_guarantee_credit",
				"prisoner",
				"universal_credit",
				"income_related_employment_and_support_allowance",
				"evidence_of_exception_or_remission_seen",
			];
			return _.some(EXEMPTION_FIELDS, function(exemptionField){
				return editing.fp17_exemptions[exemptionField]
			})
		}

	}

});
