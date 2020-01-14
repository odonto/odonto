
angular.module('opal.services').factory('Fp17Aged18InFullTimeEducation', function(toMomentFilter){

  /*

  * An FP17 can have multiple dates so look at them all starting with the earliest
  * and make sure the patient was 18 at time of treatment
  */
  return function(editing){
    if(!editing.fp17_exemptions.aged_18_in_full_time_education){
      return;
    }
    if(editing.demographics.date_of_birth){
      var otherDate = editing.fp17_incomplete_treatment.date_of_acceptance;
      otherDate = otherDate || editing.fp17_incomplete_treatment.completion_or_last_visit;

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
