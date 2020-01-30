angular.module('opal.services').factory('Fp17OAssessmentAestheticComponent', function(){
  "use strict";
  /*
  * An FP17O Assessment IOTN of 3 requires an aesthetic component
  *
  * When a patient has an assessment type "Assess & appliance fitted"
  * an aesthetic component is required.
  */

  var ASSESS_AND_APPLIANCE_FITTED = "Assess & appliance fitted"
  return function(editing){
    var assessment = editing.orthodontic_assessment;

    if(!assessment.aesthetic_component){
      if(assessment.iotn && assessment.iotn === "3"){
        return {
          orthodontic_assessment: {
            aesthetic_component: "IOTN 3 requires an aesthetic component"
          }
        }
      }
      if(assessment.assessment === ASSESS_AND_APPLIANCE_FITTED){
        return {
          orthodontic_assessment: {
            aesthetic_component: "'Assess & appliance fitted' patients require an aesthetic component"
          }
        }
      }
    }
  }
});
