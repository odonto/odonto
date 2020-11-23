angular.module('opal.services').factory('ProviderLocationNumberRequired', function(){
  "use strict";
  /*
  * Provider location should be required
  */
  return function(editing){
    var provider_location_number = editing.fp17_dental_care_provider.provider_location_number;
    if(!provider_location_number){
      return {
        fp17_dental_care_provider: {
          provider_location_number: "Provider location is required"
        }
      }
    }
  }
});
