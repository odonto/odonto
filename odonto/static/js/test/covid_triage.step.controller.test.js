describe('CovidTriageStepCtrl', function(){
  "use strict";
  var $controller;
  var scope;
  var Pathway = function(){};

  beforeEach(function(){
    module('opal.controllers');
    inject(function($injector){
      var $rootScope = $injector.get('$rootScope');
      $controller = $injector.get('$controller');

      scope = $rootScope.$new();
      scope.editing = {
        covid_triage: {}
      }
      scope.local = {
        referred: null,
      }
      scope.pathway = new Pathway();
    });
  });

  describe('setUp', function(){
    it('should set local referred to true if there is a referred to local udc reason', function(){
      scope.editing.covid_triage.referrered_to_local_udc_reason = "something";
      $controller("CovidTriageStepCtrl", {scope: scope, step: {}, episode: {}});
      expect(scope.local.referred).toBe(true);
    });

    it('should set local referred to false if there is no referred to local udc reason', function(){
      $controller("CovidTriageStepCtrl", {scope: scope, step: {}, episode: {}});
      expect(scope.local.referred).toBe(false);
    });
  });
});

