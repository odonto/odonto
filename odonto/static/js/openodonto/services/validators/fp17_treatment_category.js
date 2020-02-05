angular.module('opal.services').factory('Fp17TreatmentCategory', function(){
  "use strict";
  /*
  * If there is no treatment category we receive an
  * "No significant treatment on an EDI claim" error.
  *
  * If Free Repairt/Replacement is true, then the band
  * can only be 2, 3, Urgent
  *
  * Incomplete treatment must be the same or higher band
  * than the treatment category.
  */
  var BAND_1 = "Band 1";
  var BAND_2 = "Band 2";
  var BAND_3 = "Band 3";
  var URGENT_TREATMENT = "Urgent treatment";
  var REGULATION_11_REPLACEMENT_APPLIANCE = "Regulation 11 replacement appliance";

  var getErr = function(someStr){
    return {
      fp17_treatment_category: {
        treatment_category: someStr
      }
    }
  }

  return function(editing){
    var treatmentCategory = editing.fp17_treatment_category.treatment_category;

    if(!treatmentCategory|| treatmentCategory === ""){
      return getErr("Treatment category is required");
    }


    if(editing.fp17_other_dental_services.free_repair_or_replacement && treatmentCategory === BAND_1){
      return getErr("A patient cannot have band 1 and free repair or replacement");
    }
    if(editing.fp17_other_dental_services.further_treatment_within_2_months && treatmentCategory === URGENT_TREATMENT){
      return getErr("A patient cannot have urgent treatment and further treatment within 2 months");
    }

    var incompleteTreatment = editing.fp17_incomplete_treatment.incomplete_treatment
    if(incompleteTreatment){
      if(incompleteTreatment == BAND_2 && treatmentCategory == BAND_1){
        return getErr("The incomplete treatment band cannot be greater than the treatment category");
      }
      if(incompleteTreatment == BAND_3 && (treatmentCategory == BAND_1 || treatmentCategory == BAND_2)){
        return getErr("The incomplete treatment band cannot be greater than the treatment category");
      }
    }
  }
});
