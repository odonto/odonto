angular.module('opal.services').factory('FP17OAssessmentIOTN', function(){
  /*
  * IOTN or IOTN N/A is mandatory for any claim with assesment type of assess and review
  * or assess and refuse
  * IOTN is mandatory if assess and appliance fitted
  */
  return function(editing){
    var assessment = editing.orthodontic_assessment;
    var assessmentType = assessment.assessment;
    var ASSESS_AND_APPLIANCE_FITTED = "Assess & appliance fitted"
    var IOTN_NOT_APPLICABLE = "N/A";

    if(assessmentType){
      if(assessmentType !== ASSESS_AND_APPLIANCE_FITTED){
        if(!assessment.iotn){
          return {
            orthodontic_assessment: {
              iotn: "'" + assessmentType + "' requires an IOTN"
            }
          }
        }
      }
      else{
        if(!assessment.iotn || assessment.iotn === IOTN_NOT_APPLICABLE){
          return {
            orthodontic_assessment: {
              iotn: "'Assess & appliance fitted' requires an IOTN of 1-5"
            }
          }
        }
      }
    }
  }
});
