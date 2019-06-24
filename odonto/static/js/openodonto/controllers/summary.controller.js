angular.module('opal.controllers').controller(
  'SummaryCtrl',
  function(
      $scope, $routeParams, patient
  ){
  $scope.episode = _.findWhere(patient.episodes, {id: parseInt($routeParams.episode_id)});
});
