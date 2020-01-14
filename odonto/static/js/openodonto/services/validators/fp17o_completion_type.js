angular.module('opal.services').factory('Fp17OCompletionType', function(){
  /*
  * We have an exception of the nature
  * "Conflicting assessment and/or completion items on an EDI FP17O claim"
  *
  * The circumstances that create this are not explicit in the documentation
  *
  * It seems most likely caused by an assessment type of Assessment &
  * Refuse treatment and then a completion type which seems intuitively
  * problematic.
  *
  * Also the form guidance states "Cross this box if an
  * assessment has been performed but NHS orthodontic
  * treatment is deemed unnecessary or inappropriate."
  *
  * Which backs this up.
  */
  return function(editing){
    "use strict";
    var assessment = editing.orthodontic_assessment;
    var treatment = editing.orthodontic_treatment;
    var ASSESS_AND_REFUSE_TREATMENT = "Assess & refuse treatment"


    if(assessment.assessment === ASSESS_AND_REFUSE_TREATMENT){
      if(treatment.completion_type){
        return {
          "orthodontic_treatment": {
            "completion_type": 'There cannot be a completion type and an assessment type of "Assess & refuse treatment"'
          }
        }
      }
    }
  }
});
