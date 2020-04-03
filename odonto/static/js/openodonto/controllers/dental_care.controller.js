angular.module('opal.controllers').controller(
  'DentalCareCtrl',
  function($scope){
    "use strict";
    var DENTAL_CARE = 'Dental Care';
    var FP17 = 'FP17';
    var FP17O = 'FP17O';
    var NEW = 'New';
    var OPEN = 'Open';
  $scope.episode = _.findWhere($scope.patient.episodes, {category_name: 'Dental Care'});

  var fp17Andfp17os = _.reject($scope.patient.episodes, {category_name: 'Dental Care'});

  $scope.dentalCare = {
    newFp17: _.findWhere(fp17Andfp17os, {
      category_name: FP17, stage: NEW
    }),
    newFp17o: _.findWhere(fp17Andfp17os, {
      category_name: FP17O, stage: NEW
    }),
    hasOpenFp17: _.filter(fp17Andfp17os, {
      category_name: FP17, stage: OPEN
    }).length,
    hasOpenFp17o: _.filter(fp17Andfp17os, {
      category_name: FP17O, stage: OPEN
    }).length,
    openAndSubmittedEpisodes: _.reject(fp17Andfp17os, {
      stage: NEW
    })
  };
});
