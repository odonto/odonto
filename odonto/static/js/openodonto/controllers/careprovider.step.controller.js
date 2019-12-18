angular.module('opal.controllers').controller('CareProviderStepCtrl', function(scope, step, episode){
  "use strict";
  if(!scope.editing.fp17_dental_care_provider.performer){
    if(scope.metadata.performer.current_user){
        scope.editing.fp17_dental_care_provider.performer = scope.metadata.performer.current_user;
    }
  }
});
