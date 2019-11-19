angular.module('opal.services').factory('Fp17oUnder18', function(toMomentFilter){

  /*
  * An FP17O can have multiple dates so look at them all starting with the earliest
  * and make sure the patient was under 20 at the time (let's give some leeway)
  */
  return function(editing){
    if(!editing.fp17_exemptions.patient_under_18){
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
        if(diff > 20){
          return {
            fp17_exemptions: {
              patient_under_18: "The patient's DOB was over 18 years ago"
            }
          }
        }
      }
    }
  }
});
