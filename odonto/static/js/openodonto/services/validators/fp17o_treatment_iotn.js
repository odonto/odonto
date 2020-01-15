angular.module('opal.services').factory('TreatmentIOTN', function(){
  /*
  * Checks that the user has entered and IOTN and IOTN NA.
  *
  * Also checks that assessment IOTN/IOTN NA has not been set and
  * differs with treatment iotn
  * Note the treatment IOTN will make sure we don't enter both an assessment IOTN
  * and a treatment IOTN/treatment IOTN NA
  */
  return function(editing){
    var assessment = editing.orthodontic_assessment;
    var treatment = editing.orthodontic_treatment;

    if(assessment.iotn && treatment.iotn){
      return {
        orthodontic_treatment: {
          iotn: "There cannot be both assessment IOTN and treatment IOTN"
        }
      }
    }
  }
});
