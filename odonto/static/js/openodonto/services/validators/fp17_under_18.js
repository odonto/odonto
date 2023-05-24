
angular.module('opal.services').factory('Fp17Under18', function(toMomentFilter){
  /*
  * Returns an error if the patient is over 18 and has the under 18 box ticked.
  *
  * As of 9.7 if the patient is under 18 and the exemption is not raised
  * then an error is returned.
  *
  * An FP17 can have multiple dates so look at them all starting with the earliest
  * and make sure the patient was under 19 at the time
  */
  return function(editing){
    if(editing.demographics.date_of_birth){
      var otherDate = editing.fp17_incomplete_treatment.date_of_acceptance;
      otherDate = otherDate || editing.fp17_incomplete_treatment.completion_or_last_visit;

      if(otherDate){
        var otherMoment = toMomentFilter(otherDate);

        var dobMoment = toMomentFilter(editing.demographics.date_of_birth);
        var eighteenBirthday = dobMoment.add(18, 'years');

        // if the patient is over 18, return an error message
        // if the patient has the under 18 exemption ticked
        if(otherMoment.diff(eighteenBirthday, "days") >= 0){
          if(editing.fp17_exemptions.patient_under_18){
            return {
              fp17_exemptions: {
                patient_under_18: "This patient is not under 18"
              }
            }
          }
        }
        // if the patient is under 18, return an error message
        // if the patient has the under 18 exemption is not ticked
        else{
          if(!editing.fp17_exemptions.patient_under_18){
            return {
              fp17_exemptions: {
                patient_under_18: "This patient is under 18"
              }
            }
          }
        }
      }
    }
  }
});
