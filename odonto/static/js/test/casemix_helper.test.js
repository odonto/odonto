describe('CaseMixHelper', function() {
  "use strict";
  var $rootScope;
  var $controller;
  var controller;
  var scope;
  var caseMix = {};

  beforeEach(function(){
    module('opal.controllers');
    inject(function($injector){
      $rootScope = $injector.get('$rootScope');
      $controller = $injector.get('$controller');
    });
    scope = $rootScope.$new();
    controller = $controller("CaseMixHelper", {scope: scope});
    caseMix = {
      ability_to_communicate: "0",
      ability_to_cooperate: "0",
      medical_status: "0",
      oral_risk_factors: "0",
      access_to_oral_care: "0",
      legal_and_ethical_barriers_to_care: "0",
    }
  });

  describe('getCaseMixScores', function(){
    it('should return 0 if there is no higher code', function(){
      expect(controller.maxCode(caseMix)).toBe("0");
    });

    it('should return A if A is the higher code', function(){
      caseMix.ability_to_cooperate = "A";
      expect(controller.maxCode(caseMix)).toBe("A");
    });

    it('should return C if C is the highest code', function(){
      caseMix.legal_and_ethical_barriers_to_care = "A";
      caseMix.medical_status = "C";
      expect(controller.maxCode(caseMix)).toBe("C");
    });
  });

  describe('totalScore', function(){
    it('should return 0 if there is no higher code', function(){
      expect(controller.totalScore(caseMix)).toBe(0);
    });

    it('should return 3 if A is the higher code', function(){
      caseMix.ability_to_cooperate = "A";
      expect(controller.totalScore(caseMix)).toBe(3);;
    });

    it('should return the sum of multiple codes', function(){
      caseMix.ability_to_cooperate = "A";
      caseMix.access_to_oral_care = "C";
      expect(controller.totalScore(caseMix)).toBe(11);;
    });
  });

  describe('band', function(){
    it('should return standard patient if there is no higher code', function(){
      expect(controller.band(caseMix)).toBe("Standard patient");
    });

    it('should return some complexity if there is some complexity', function(){
      caseMix.ability_to_cooperate = "A";
      expect(controller.band(caseMix)).toBe("Some complexity");
    });

    it('should return moderate complexity if there is moderate complexity', function(){
      caseMix.ability_to_cooperate = "A";
      caseMix.access_to_oral_care = "C";
      expect(controller.band(caseMix)).toBe("Moderate complexity");
    });

    it('should return severe complexity if there is severe complexity', function(){
      caseMix.ability_to_cooperate = "A";
      caseMix.access_to_oral_care = "C";
      caseMix.oral_risk_factors = "C";
      expect(controller.band(caseMix)).toBe("Severe complexity");
    });

    it('should return extreme complexity if there is extreme complexity', function(){
      caseMix.ability_to_communicate = "B";
      caseMix.ability_to_cooperate = "A";
      caseMix.access_to_oral_care = "C";
      caseMix.oral_risk_factors = "C";
      caseMix.legal_and_ethical_barriers_to_care = "C";
      expect(controller.band(caseMix)).toBe("Extreme complexity");
    });
  });
});