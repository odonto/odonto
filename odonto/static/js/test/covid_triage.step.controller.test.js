describe('CovidTriageStepCtrl', function(){
  "use strict";
  var $controller;
  var scope;

  beforeEach(function(){
    module('opal.controllers');
    inject(function($injector){
      var $rootScope = $injector.get('$rootScope');
      $controller = $injector.get('$controller');

      scope = $rootScope.$new();
      scope.editing = {
        covid_triage: {}
      }
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

    it('should set the covid triage time of contact to a date on local.time_of_contact if populated', function(){
      scope.editing.covid_triage.time_of_contact = "20:00";
      $controller("CovidTriageStepCtrl", {scope: scope, step: {}, episode: {}});
      expect(scope.local.time_of_contact.getHours()).toBe(20);
      expect(scope.local.time_of_contact.getMinutes()).toBe(0);
    });
  });

  describe('preSave', function(){
    it('should put the time onto the scope in the form we expect', function(){
      var timeOfContact = new Date();
      timeOfContact.setHours(10);
      timeOfContact.setMinutes(30);
      var toSave = {covid_triage: {}};
      $controller("CovidTriageStepCtrl", {scope: scope, step: {}, episode: {}});
      scope.local = {time_of_contact: timeOfContact};
      scope.preSave(toSave);
      expect(toSave.covid_triage.time_of_contact).toBe("10:30");
    });

    it('should not set time if there is nothing on the scope', function(){
      var timeOfContact = new Date();
      timeOfContact.setHours(10);
      timeOfContact.setMinutes(30);
      var toSave = {covid_triage: {}};
      $controller("CovidTriageStepCtrl", {scope: scope, step: {}, episode: {}});
      scope.preSave(toSave);
      expect(toSave.covid_triage).toEqual({});
    });
  });
});

