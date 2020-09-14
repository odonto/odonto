
angular.module('opal.services').factory('Fp17Under18', function(toMomentFilter){

  /*
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
        var eighteenBirthday = dobMoment.add(18, 'years');

        if(otherMoment.diff(eighteenBirthday, "days") >= 0){
          return {
            fp17_exemptions: {
              patient_under_18: "This patient is not under 18"
            }
          }
        }
      }
    }
  }
});
