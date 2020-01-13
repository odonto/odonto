angular.module('opal.services').factory('Fp17TreatmentCategory', function(){

  /*
  * If there is no treatment category we receive an
  * "No significant treatment on an EDI claim" error.
  *
  * If Free Repairt/Replacement is true, then the band
  * can only be 2, 3, Urgent
  */
  var BAND_1 = "Band 1"
  var URGENT_TREATMENT = "Urgent treatment"

  return function(editing){
    if(!editing.fp17_treatment_category.treatment_category || editing.fp17_treatment_category.treatment_category === ""){
      return {
        fp17_treatment_category: {
          treatment_category: "Treatment category is required"
        }
      }
    }

    if(editing.fp17_other_dental_services.free_repair_or_replacement && editing.fp17_treatment_category.treatment_category === BAND_1){
      return {
        fp17_treatment_category: {
          treatment_category: "A patient cannot have band 1 and free repair or replacement"
        }
      }
    }
    if(editing.fp17_other_dental_services.further_treatment_within_2_months && editing.fp17_treatment_category.treatment_category === URGENT_TREATMENT){
      return {
        fp17_treatment_category: {
          treatment_category: "A patient cannot have urgent treatment and further treatment within 2 months"
        }
      }
    }
  }
});
