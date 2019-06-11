angular.module('opal.controllers').controller('RedirectIfValid', function(scope, step, episode, $timeout, $rootScope){
  "use strict";
  $rootScope.isFormValid = null;

  $timeout(function(){
    scope.form.$setSubmitted();
    if(scope.form.$valid){
      $rootScope.isFormValid = true;
    }
    else{
      $rootScope.isFormValid = false;
    }
  });
});
