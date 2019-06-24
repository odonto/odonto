angular
  .module("opal.services")
  .factory("DemographicsSearch", function($http, $window, ngProgressLite) {
    "use strict";
    /*
     * The demographics search used by the find patient
     * pathway.
     */

    // we have four call backs that we are expecting

    // patient is found in odonto
    var PATIENT_FOUND_IN_APPLICATION = "patient_found_in_application";

    // patient is not found
    var PATIENT_NOT_FOUND = "patient_not_found";

    var expectedStatuses = [
      PATIENT_FOUND_IN_APPLICATION,
      PATIENT_NOT_FOUND
    ];

    var find = function(apiEndPoint, hospitalNumber, findPatientOptions) {
      ngProgressLite.set(0);
      ngProgressLite.start();
      var callBackNames = _.keys(findPatientOptions);
      _.each(callBackNames, function(key) {
        if (expectedStatuses.indexOf(key) === -1) {
          throw "unknown call back";
        }
      });
      var patientUrl =
        apiEndPoint + "?nhs_number=" + encodeURIComponent(hospitalNumber);
      $http.get(patientUrl).then(
        function(response) {
          ngProgressLite.done();
          if (response.data.status == PATIENT_FOUND_IN_APPLICATION) {
            findPatientOptions[PATIENT_FOUND_IN_APPLICATION](
              response.data.patient
            );
          } else if (response.data.status == PATIENT_NOT_FOUND) {
            findPatientOptions[PATIENT_NOT_FOUND]();
          } else {
            $window.alert("DemographicsSearch could not be loaded");
          }
        },
        function() {
          ngProgressLite.done();
          $window.alert("DemographicsSearch could not be loaded");
        }
      );
    };

    return {
      find: find
    };
  });
