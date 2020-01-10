angular.module('opal.services').factory('Fp17TreatmentCategory', function(){

  /*
  * If there is no treatment category we receive an
  * "No significant treatment on an EDI claim" error.
  */
  return function(editing){
    if(!editing.fp17_treatment_category.treatment_category || editing.fp17_treatment_category.treatment_category === ""){
      return {
        fp17_treatment_category: {
          treatment_category: "Treatment category is required"
        }
      }
    }
  }
});
