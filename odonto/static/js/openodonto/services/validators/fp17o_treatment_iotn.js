angular.module('opal.services').factory('TreatmentIOTN', function(){
  /*
  * Checks that the user has not entered an assessment IOTN and a treatment IOTN.
  */
  return function(editing){
    var assessment = editing.orthodontic_assessment;
    var treatment = editing.orthodontic_treatment;

    if(assessment.iotn && treatment.iotn){
      return {
        orthodontic_treatment: {
          iotn: "There cannot be both assessment IOTN and completion IOTN"
        }
      }
    }
  }
});
