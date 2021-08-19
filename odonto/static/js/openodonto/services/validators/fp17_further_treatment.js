
angular.module('opal.services').factory('Fp17FurtherTreatment', function(toMomentFilter){
  "use strict";

  /*
  * If further treatment is ticked there must be an episode within the
  * 2 months prior to the date of acceptance
  *
  * Valid claims exclude urgent (9150 4), incomplete (9164),
  * Further treatment within 2 months (9163) or a lower band
  */

  var toErr = function(someStr){
    return {
      fp17_other_dental_services: {
        further_treatment_within_2_months: someStr
      }
    }
  }

  var BAND_1 = "Band 1";
  var BAND_2 = "Band 2";
  var BAND_3 = "Band 3";
  var BANDS = [BAND_1, BAND_2, BAND_3];

  return function(editing, step){
    var further_treatment_within_2_months = editing.fp17_other_dental_services.further_treatment_within_2_months;
    var dateOfAcceptance = toMomentFilter(editing.fp17_incomplete_treatment.date_of_acceptance);
    var treatmentCategory = editing.fp17_treatment_category.treatment_category;

    if(!further_treatment_within_2_months){
      return;
    }

    if(!treatmentCategory){
      return;
    }

    // date of acceptance is required but this is validated elsewhere
    if(!dateOfAcceptance){
      return;
    }

    if(!_.contains(BANDS, treatmentCategory)){
      return toErr('Requires Band 1, 2 or 3');
    }

    var twoMonthsAgo = moment(dateOfAcceptance).subtract(2, "month");

    var furtherInformation = _.map(step.further_treatment_information, function(fti){
      fti.completion_or_last_visit = toMomentFilter(fti.completion_or_last_visit)
      return fti;
    });

    var beforeEpisode = [];

    _.each(furtherInformation, function(fti){
      if(fti.completion_or_last_visit.isBefore(dateOfAcceptance, "d") && fti.completion_or_last_visit.isAfter(twoMonthsAgo, "d")){
        beforeEpisode.push(fti);
      }
    });

    if(!beforeEpisode.length){
      return toErr("No prior episode found in the last two months")
    }

    /*
    * We exclude treatments if they are of a lower band.
    * if previous band was 2 for example and this episodes band is 1
    * That would be an error.
    *
    * Anything not a band outranks anything that is.
    * Urgent treatments are excluded by the server.
    */
    var existingTreatmentCategories = _.pluck(beforeEpisode, "category");
    var hasError = true;

    _.each(existingTreatmentCategories, function(tc){
      var rank = BANDS.indexOf(tc);
      if(rank === -1){
        hasError = false;
      }
      if(rank >= BANDS.indexOf(treatmentCategory)){
        hasError = false
      }
    });

    if(hasError){
      return toErr("No prior episode found with an appropriate category");
    }
  }
});
