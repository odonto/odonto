angular.module('opal.services').factory('Fp17TreatmentCategory', function(toMomentFilter,recordLoader){
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
  *
  */
  var BAND_1 = "Band 1";
  var BAND_2 = "Band 2";
  var BAND_3 = "Band 3";
  var URGENT_TREATMENT = "Urgent treatment";
  var REGULATION_11_REPLACEMENT_APPLIANCE = "Regulation 11 replacement appliance";
  var schema = null;
  recordLoader.load().then(function(s){
    schema = s;
  });

  var getErr = function(someStr){
    someStr = someStr.charAt(0).toUpperCase() + someStr.slice(1);
    return {
      fp17_treatment_category: {
        treatment_category: someStr
      }
    }
  }

  var getClinicDataSetTitles = function(fieldNames){
    /*
    * Takes an array of fp17 clinical data set field names
    * returns their display names.
    */
    // this should never happen
    if(!schema){
      return _.map(fieldNames, function(fn){ return fn.replace("_", " ") });
    }
    var cdsSchema = schema['fp17_clinical_data_set'];
    return _.map(fieldNames, function(fn){
      return _.findWhere(cdsSchema.fields, {name: fn}).title.toLowerCase();
    });
  }


  function cdsBandValidation(editing){
    /*
    * There is a concept of a CDS Band as defined here.
    * https://www.nhsbsa.nhs.uk/sites/default/files/2022-05/Clinical_Data_Set_validation_rules_from_1_April_2022_V1.1_England.pdf
    */

    var BANDS_TO_FIELDS = {
      0: ['antibiotic_items_prescribed'],
      1: [
          'examination',
          'scale_and_polish',
          'fluoride_varnish',
          'fissure_sealants',
          'radiographs_taken',
          'phased_treatment',
          'other_treatment',
        ],
      2: [
        'endodontic_treatment',
        'permanent_fillings',
        'extractions',
        'pre_formed_crowns',
        'advanced_perio_root_surface_debridement',
        'denture_additions_reline_rebase',
      ],
      3: [
        'crowns_provided',
        'upper_denture_acrylic',
        'lower_denture_acrylic',
        'upper_denture_metal',
        'lower_denture_metal',
        'veneers_applied',
        'inlays',
        'bridges_fitted',
        'custom_made_occlusal_appliance'
      ]
    }

    var clinical_dataset = editing.fp17_clinical_data_set;
    var treatment_category = editing.fp17_treatment_category.treatment_category;

    var patientsTreamentsOfBandX = function(bandNumber){
      /*
      * When given a band e.g. 2, return
      * the patient's band 2 treatments
      */
      var populated = [];
      _.each(BANDS_TO_FIELDS[String(bandNumber)], function(field){
        if(clinical_dataset[field]){
          populated.push(field);
        }
      });
      return populated;
    }

    // If a patient is referred to AMS the below checks do not apply
    if(clinical_dataset.referral_for_advanced_mandatory_services_band){
      return;
    }

    var treatmentsOfBand1 = patientsTreamentsOfBandX(1);
    var treatmentsOfBand2 = patientsTreamentsOfBandX(2);
    var treatmentsOfBand3 = patientsTreamentsOfBandX(3);

    // CDS Band 0
    // Allowed on any claim, but urgent claims need more than a band 0
    // ie its an urgent claim and its only antibiotic_items_prescribed
    // return an error
    if(treatment_category === URGENT_TREATMENT){
      if(!treatmentsOfBand1.length && !treatmentsOfBand2.length && !treatmentsOfBand3.length){
        return getErr(
          'Additional clinical dataset items are required to justify an Urgent Treatment band'
        )
      }
    }

    // CDS Band 3
    // Allowed on Band 3 or Reg 11
    // There must be at least
    // one of these codes
    // present if Band 3
    if(treatment_category === BAND_3){
      if(!treatmentsOfBand3.length){
        return getErr(
          'One of ' + getClinicDataSetTitles(BANDS_TO_FIELDS["3"]).join(', ') + 'are required to justify a band 3'
        )
      }
    }
    else if(treatmentsOfBand3.length && treatment_category !== REGULATION_11_REPLACEMENT_APPLIANCE){
      var requires = "require"
      if(treatmentsOfBand3.length === 1){
        requires = "requires"
      }
      return getErr(
        getClinicDataSetTitles(treatmentsOfBand3).join(", ") + " " + requires + " a band 3"
      )
    }

    // CDS Band 2
    // Allowed on Band 2, 3, Reg 11 or Urgent only
    // There must be at least one of these codes present if
    // Band 2 is claimed
    if(treatment_category === BAND_2){
      if(!treatmentsOfBand2.length){
        return getErr(
          'To justify a band 2, at least one of the following is required: ' + getClinicDataSetTitles(BANDS_TO_FIELDS["2"]).join(', ')
        )
      }
    }
    else if(treatment_category !== URGENT_TREATMENT && treatment_category !== REGULATION_11_REPLACEMENT_APPLIANCE){
      if(treatmentsOfBand2.length && !treatmentsOfBand3.length){
        var requires = "require"
        if(treatmentsOfBand2.length === 1){
          requires = "requires"
        }
        return getErr(
          getClinicDataSetTitles(treatmentsOfBand2).join(", ") + " " + requires + " a band 2"
        )
      }
    }


    // CDS Band 1
    // Allowed on Band 1, 2, 3, Reg 11 or Urgent only
    // There must be at least one of these codes present if
    // Treatment Band 1 is claimed,
    if(
      treatment_category !== BAND_1 &&
      treatment_category !== URGENT_TREATMENT &&
      treatment_category !== REGULATION_11_REPLACEMENT_APPLIANCE){
      if(treatmentsOfBand1.length && !treatmentsOfBand2.length && !treatmentsOfBand3.length){
        var requires = "require"
        if(treatmentsOfBand1.length === 1){
          requires = "requires"
        }
        return getErr(
          getClinicDataSetTitles(treatmentsOfBand1).join(", ") + " " + requires + " a band 1"
        )
      }
    }
    if(treatment_category === BAND_1 && !treatmentsOfBand1.length){
      return getErr(
        'To justify a band 1, at least one of the following is required: ' + getClinicDataSetTitles(BANDS_TO_FIELDS["1"]).join(', ')
      )
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

    return cdsBandValidation(editing);
  }
});
