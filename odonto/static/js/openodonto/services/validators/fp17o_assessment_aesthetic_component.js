angular.module('opal.services').factory('Fp17OAssessmentAestheticComponent', function(){
  /*
  * An FP17O Assessment IOTN of 3 requires an aesthetic component
  */
  return function(editing){
    var assessment = editing.orthodontic_assessment;

    if(assessment.iotn && assessment.iotn === "3"){
      if(!assessment.aesthetic_component){
        return {
          orthodontic_assessment: {
            aesthetic_component: "IOTN 3 requires an aesthetic component"
          }
        }
      }
    }
  }
});
