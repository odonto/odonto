angular.module('opal.services').factory('Fp17OTreatmentAestheticComponent', function(){
  /*
  * An FP17O Completion IOTN of 3 requires an aesthetic component
  */
  return function(editing){
    var treatment = editing.orthodontic_treatment;

    if(treatment.iotn && treatment.iotn === "3"){
      if(!treatment.aesthetic_component){
        return {
          orthodontic_treatment: {
            aesthetic_component: "IOTN 3 requires an aesthetic component"
          }
        }
      }
    }
  }
});
