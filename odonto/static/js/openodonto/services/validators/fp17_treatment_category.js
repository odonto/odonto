angular.module('opal.services').factory('Fp17TreatmentCategory', function(toMomentFilter){
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
  *
  * We believe a charge is required for reg 11
  * This because we've had a rejection without a charge
  * described as
  * "inappropriate patient's charge accompanying Reg 11"
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

  return function(editing, step){
    var treatmentCategory = editing.fp17_treatment_category.treatment_category;

    if(!treatmentCategory|| treatmentCategory === ""){
      return getErr("Treatment category is required");
    }

    if(editing.fp17_other_dental_services.free_repair_or_replacement && treatmentCategory === BAND_1){
      return getErr("A patient cannot have band 1 and free repair or replacement");
    }

    if(editing.fp17_other_dental_services.free_repair_or_replacement){
      /*
      * To claim a free repair or replacement
      * "a previous claim must be present with a higher or equal band within
      * the previous 12 months."
      */
      var completion = toMomentFilter(editing.fp17_incomplete_treatment.completion_or_last_visit)
      if(completion){
        var lastYear = toMomentFilter(completion).subtract(1, "years").toDate()
        var err = getErr('Free repair or replacement requires a band equal or lower to a previous treatment in the last 12 months');
        _.each(step.free_repair_replacement_information, function(frr){
          frr.completion_or_last_visit = toMomentFilter(frr.completion_or_last_visit).toDate();
          if(frr.completion_or_last_visit >= lastYear && frr.completion_or_last_visit <= completion){
            if(treatmentCategory == BAND_2){
              if(frr.category == BAND_2 || frr.category == BAND_3){
                err = null;
              }
            }
            if(treatmentCategory == BAND_3){
              if(frr.category == BAND_3){
                err = null;
              }
            }
          }
        });
        if(err){
          return err
        }
      }
    }

    if(editing.fp17_other_dental_services.further_treatment_within_2_months && treatmentCategory === URGENT_TREATMENT){
      return getErr("A patient cannot have urgent treatment and further treatment within 2 months");
    }

    var incompleteTreatment = editing.fp17_incomplete_treatment.incomplete_treatment
    if(incompleteTreatment){
      if(treatmentCategory == URGENT_TREATMENT){
        return getErr("Urgent treatment cannot have an incomplete treatment");
      }
      if(incompleteTreatment == BAND_2){
        if(treatmentCategory == BAND_1){
          return getErr("The incomplete treatment band cannot be greater than the treatment category band");
        }
      }

      if(incompleteTreatment == BAND_3){
        if(treatmentCategory == BAND_1 || treatmentCategory == BAND_2){
          return getErr("The incomplete treatment band cannot be greater than the treatment category band");
        }
      }
    }

    if(treatmentCategory === REGULATION_11_REPLACEMENT_APPLIANCE){
      if(!editing.fp17_exemptions.patient_charge_collected){
        return getErr('A patient charge is required for reg 11')
      }
    }
  }
});
