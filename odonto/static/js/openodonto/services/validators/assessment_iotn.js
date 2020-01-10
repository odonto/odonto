angular.module('opal.services').factory('AssessmentIOTN', function(){
  /*
  * Checks that the user has entered and IOTN and IOTN NA.
  *
  * Note the treatment IOTN will make sure we don't enter both an assessment IOTN
  * and a treatment IOTN/treatment IOTN NA
  */
  return function(editing){
    if(editing.orthodontic_assessment.iotn){
      if(editing.orthodontic_assessment.iotn_not_applicable){
        return {
          orthodontic_assessment: {
            iotn_not_applicable: "There cannot be both IOTN and IOTN not applicable"
          }
        }
      }
    }
  }
});
