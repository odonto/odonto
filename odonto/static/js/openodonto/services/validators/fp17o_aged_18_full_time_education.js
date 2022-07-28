
angular.module('opal.services').factory('Fp17OAged18InFullTimeEducation', function(toMomentFilter){

  /*
  * An FP17O can have multiple dates so look at them all starting with the earliest
  * and make sure the patient was 18 at time of treatment
  */
  return function(editing){
    // completion types do not need to validate age.
    if(editing.orthodontic_treatment.completion_type){
      return;
    }


    if(!editing.fp17_exemptions.aged_18_in_full_time_education){
      return;
    }
    if(editing.demographics.date_of_birth){
      var otherDate = editing.orthodontic_assessment.date_of_referral;
      otherDate = otherDate || editing.orthodontic_assessment.date_of_assessment;
      otherDate = otherDate || editing.orthodontic_assessment.date_of_appliance_fitted;
      otherDate = otherDate || editing.orthodontic_treatment.date_of_completion;

      if(otherDate){
        var otherMoment = toMomentFilter(otherDate);

        var dobMoment = toMomentFilter(editing.demographics.date_of_birth);
        var diff = otherMoment.diff(dobMoment, "years", false);
        if(diff !== 18){
          return {
            fp17_exemptions: {
              aged_18_in_full_time_education: "The patient was not 18"
            }
          }
        }
      }
    }
  }
});
