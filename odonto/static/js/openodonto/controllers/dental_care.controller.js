angular.module('opal.controllers').controller(
  'DentalCareCtrl',
  function($scope){
    "use strict";
    var FP17 = 'FP17';
    var FP17O = 'FP17O';
    var COVID_TRIAGE = "COVID_TRIAGE"
    var NEW = 'New';
    var OPEN = 'Open';
  $scope.episode = _.findWhere($scope.patient.episodes, {category_name: 'Dental Care'});

  var fp17CovidTriageAndfp17os = _.reject($scope.patient.episodes, {category_name: 'Dental Care'});

  $scope.dentalCare = {
    newFp17: _.findWhere(fp17CovidTriageAndfp17os, {
      category_name: FP17, stage: NEW
    }),
    newFp17o: _.findWhere(fp17CovidTriageAndfp17os, {
      category_name: FP17O, stage: NEW
    }),
    newCovidTriage: _.findWhere(fp17CovidTriageAndfp17os, {
      category_name: COVID_TRIAGE, stage: NEW
    }),
    hasOpenFp17: !!_.filter(fp17CovidTriageAndfp17os, {
      category_name: FP17, stage: OPEN
    }).length,
    hasOpenFp17o: !!_.filter(fp17CovidTriageAndfp17os, {
      category_name: FP17O, stage: OPEN
    }).length,
    hasCovidTriage: !!_.filter(fp17CovidTriageAndfp17os, {
      category_name: COVID_TRIAGE, stage: OPEN
    }).length,
    openAndSubmittedEpisodes: _.reject(fp17CovidTriageAndfp17os, {
      stage: NEW
    })
  };
});
