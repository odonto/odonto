angular
  .module("opal.controllers")
  .controller("LookupPatientCrl", function(
    scope,
    step,
    DemographicsSearch,
    $location,
    $window
  ) {
    "use strict";

    scope.lookup_nhs_number = function() {
      DemographicsSearch.find(
        step.search_end_point,
        scope.editing.demographics.nhs_number,
        {
          // we can't find the patient on either odonto or the hospital demographcis
          patient_not_found: scope.new_patient,
          // the patient has been entered into odonto before
          patient_found_in_application: scope.new_for_patient,
        }
      );
    };

    this.initialise = function(scope) {
      if ($location.search().nhs_number) {
        scope.editing.demographics = {
          nhs_number: $location.search().nhs_number
        };
        scope.lookup_nhs_number();
      } else {
        scope.state = "initial";
        scope.editing.demographics = {
          nhs_number: undefined
        };
      }
    };

    scope.new_patient = function() {
      scope.hideFooter = false;
      scope.state = "editing_demographics";
    };

    scope.new_for_patient = function(patient) {
      $window.location.href = "/#/patient/" + patient.id + "/";
    };

    scope.preSave = function(editing) {
      // this is not great
      if (editing.demographics && editing.demographics.patient_id) {
        scope.pathway.save_url =
          scope.pathway.save_url + "/" + editing.demographics.patient_id;
      }
    };
    this.initialise(scope);
  });
