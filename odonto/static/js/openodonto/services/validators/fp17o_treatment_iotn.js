angular.module('opal.services').factory('TreatmentIOTN', function(){
  /*
  * Checks that the user has not entered an assessment IOTN and a treatment IOTN.
  *
  * IOTN 1-5 or IOTN N/A is now mandatory for any claim with completion type of treatment abandoned
  * or treatment discontinued
  * IOTN 1-5 is mandatory if treatment completed
  */
  return function(editing){
    var assessment = editing.orthodontic_assessment;
    var treatment = editing.orthodontic_treatment;
    var completionType = treatment.completion_type;
    var TREATMENT_COMPLETED = "Treatment completed"
    var IOTN_NOT_APPLICABLE = "N/A";

    if(assessment.iotn && treatment.iotn){
      return {
        orthodontic_treatment: {
          iotn: "There cannot be both assessment IOTN and completion IOTN"
        }
      }
    }

    if(completionType){
      if(completionType !== TREATMENT_COMPLETED){
        if(!treatment.iotn){
          return {
            orthodontic_treatment: {
              iotn: "'" + completionType + "' requires an IOTN"
            }
          }
        }
      }
      else{
        if(!treatment.iotn || treatment.iotn === IOTN_NOT_APPLICABLE){
          return {
            orthodontic_treatment: {
              iotn: "'Treatment completed' requires an IOTN of 1-5"
            }
          }
        }
      }
    }
  }
});
