describe('DentalCareCtrl', function(){
  "use strict";
  var $scope, $controller

  beforeEach(function(){
    module('opal.controllers');
    inject(function($injector){
      var $rootScope = $injector.get('$rootScope');
      $controller = $injector.get('$controller');

      $scope = $rootScope.$new();
      $scope.patient = {episodes: {}};
      $scope.patient.episodes = {
        1: {
          category_name: "FP17",
          stage: "Submitted"
        },
        2: {
          category_name: "FP17O",
          stage: "Submitted"
        },
        3: {
          category_name: "FP17",
          stage: "Open"
        },
        4: {
          category_name: "FP17O",
          stage: "Open"
        },
        5: {
          category_name: "FP17",
          stage: "New"
        },
        6: {
          category_name: "FP17O",
          stage: "New"
        },
      }
    });
  });

  it('should populate the new FP17', function(){
    $controller("DentalCareCtrl", {$scope: $scope})
    expect($scope.dentalCare.newFp17).toBe($scope.patient.episodes[5]);
  });

  it('should populate the new FP17O', function(){
    $controller("DentalCareCtrl", {$scope: $scope})
    expect($scope.dentalCare.newFp17o).toBe($scope.patient.episodes[6]);
  });

  it('should populate hasOpenFp17  ', function(){
    $controller("DentalCareCtrl", {$scope: $scope})
    expect($scope.dentalCare.hasOpenFp17).toBe(true);
  });
});