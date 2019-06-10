angular.module('opal.controllers').controller('RedirectIfValid', function(scope, step, episode, $rootScope){
  "use strict";

  $rootScope.baseSummaryUrl = step.base_summary_url;

  setTimeout(function(){
    scope.form.$setSubmitted();
    if(scope.form.$valid){
      $rootScope.isFormValid = true;
    }
    else{
      $rootScope.isFormValid = false;
    }
  }, 1);
});
