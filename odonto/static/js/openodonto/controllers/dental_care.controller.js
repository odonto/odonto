angular.module('opal.controllers').controller(
  'DentalCareCtrl',
  function($scope){
    "use strict";
    var FP17 = 'FP17';
    var FP17O = 'FP17O';
    var COVID_TRIAGE = "COVID-19 triage"
    var NEW = 'New';
    var OPEN = 'Open';
  $scope.episode = _.findWhere($scope.patient.episodes, {category_name: 'Dental Care'});

  var nonDentalCare = _.reject($scope.patient.episodes, {category_name: 'Dental Care'});

  $scope.showCovidTriage = function(episode, userHasPermission){
    if(episode.category_name !==  COVID_TRIAGE){
      return true;
    }
    if(userHasPermission){
      return true;
    }
    return false
  }

  $scope.dentalCare = {
    newFp17: _.findWhere(nonDentalCare, {
      category_name: FP17, stage: NEW
    }),
    newFp17o: _.findWhere(nonDentalCare, {
      category_name: FP17O, stage: NEW
    }),
    newCovidTriage: _.findWhere(nonDentalCare, {
      category_name: COVID_TRIAGE, stage: NEW
    }),
    hasOpenFp17: !!_.filter(nonDentalCare, {
      category_name: FP17, stage: OPEN
    }).length,
    hasOpenFp17o: !!_.filter(nonDentalCare, {
      category_name: FP17O, stage: OPEN
    }).length,
    hasCovidTriage: !!_.filter(nonDentalCare, {
      category_name: COVID_TRIAGE, stage: OPEN
    }).length,
    openAndSubmittedEpisodes: _.reject(nonDentalCare, {
      stage: NEW
    })
  };
});
