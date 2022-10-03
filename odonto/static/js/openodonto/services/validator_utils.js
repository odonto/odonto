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
		}
	}

});
