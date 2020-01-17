angular.module('opal.services').factory('Fp17O_IOTN', function(toMomentFilter){

  /*
  * If assess and review or assess and refuse, IOTN or IOTN NA must be present
  * If assess and appliance permitted IOTN NA is not permitted IOTN is required
  *
  * If ortho abandoned or ortho discontinued, IOTN or IOTN NA must be present
  * If ortho completed, IOTN NA is not permitted IOTN is required
  *
  * IOTN and IOTN NA are mutually exclusive
  * An FP17 can have multiple dates so look at them all starting with the earliest
  * and make sure the patient was under 19 at the time
  */
  return function(editing){
    if(!editing.fp17_exemptions.patient_under_18){
      return;
    }
    if(editing.demographics.date_of_birth){
      var otherDate = editing.fp17_incomplete_treatment.date_of_acceptance;
      otherDate = otherDate || editing.fp17_incomplete_treatment.completion_or_last_visit;

      if(otherDate){
        var otherMoment = toMomentFilter(otherDate);

        var dobMoment = toMomentFilter(editing.demographics.date_of_birth);
        var diff = otherMoment.diff(dobMoment, "years", false);
        if(diff > 18){
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
