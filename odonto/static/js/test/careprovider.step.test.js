describe('CareProviderStepCtrl', function(){
  "use strict";
  var $controller;
  var controller;
  var scope;

  beforeEach(function(){
    module('opal.controllers');
    inject(function($injector){
      var $rootScope = $injector.get('$rootScope');
      $controller = $injector.get('$controller');

      scope = $rootScope.$new();
      scope.editing = {
        fp17_dental_care_provider: {}
      }

      scope.metadata = {
        performer: {}
      }
    });
  });

  it('should set the user if the user is not already set', function(){
    scope.metadata.performer.current_user = "Betty";
    controller = $controller("CareProviderStepCtrl", {scope: scope, step: {}, episode: {}});
    expect(scope.editing.fp17_dental_care_provider.performer).toBe('Betty');
  });

  it('should not override the existing user if the user is already set', function(){
    scope.editing.fp17_dental_care_provider.performer = "Sue"
    scope.metadata.performer.current_user = "Betty";
    controller = $controller("CareProviderStepCtrl", {scope: scope, step: {}, episode: {}});
    expect(scope.editing.fp17_dental_care_provider.performer).toBe('Sue');
  });

  it('should not set the user if the user is not set', function(){
    controller = $controller("CareProviderStepCtrl", {scope: scope, step: {}, episode: {}});
    expect(scope.editing.fp17_dental_care_provider.performer).toBeUndefined();
  });
});

