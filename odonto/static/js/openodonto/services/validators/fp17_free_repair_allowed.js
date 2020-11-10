angular.module('opal.services').factory('Fp17FreeRepairAllowed', function(toMomentFilter){
  "use strict";
  /*
  * A free repair is allow if there is a previous step that is of
  * a higher band within the last 12 months.
  *
  * Only applies to Band 1, 2 or 3
  */
  return function(editing, step){
    if(!editing.fp17_other_dental_services.free_repair_or_replacement){
      return;
    }
    if(!editing.fp17_incomplete_treatment.completion_or_last_visit){
      return;
    }

    var bandWeightings = {
      "Urgent treatment": 0,
      "Band 1": 1,
      "Band 2": 2,
      "Band 3": 3
    }

    var band = editing.fp17_treatment_category.treatment_category;

    if(!bandWeightings[band]){
      return {
        fp17_other_dental_services: {
          free_repair_or_replacement: "Inappropriate treatment category for a free repair"
        }
      }
    }

    var signOffDate = toMomentFilter(editing.fp17_incomplete_treatment.completion_or_last_visit);
    var twelveMonthsAgo = moment(signOffDate).subtract(12, "M");
    var band = editing.fp17_treatment_category.treatment_category;
    var otherDatesToBands = step.submitted_bands;

    var highestBandIn12Months = null;

    _.each(otherDatesToBands, function(dateAndCategory){
      var otherSignOffDate = toMomentFilter(dateAndCategory[0]);
      var weighting = bandWeightings[dateAndCategory[1]]

      // over 12 months ago, not important
      if(otherSignOffDate.toDate() < twelveMonthsAgo.toDate()){
        return;
      }

      if(otherSignOffDate.toDate() > signOffDate.toDate()){
        return;
      }

      // ie a category we don't care about
      if(!weighting){
        return;
      }

      if(!highestBandIn12Months){
        highestBandIn12Months = weighting;
      }
      else if(highestBandIn12Months < weighting){
        highestBandIn12Months = weighting;
      }
    });

    if(!highestBandIn12Months || !bandWeightings[band] || highestBandIn12Months < bandWeightings[band]){
      return {
        fp17_other_dental_services: {
          free_repair_or_replacement: "No previous guarenteed item for this patient"
        }
      }
    }
  }
});
