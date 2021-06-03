angular.module('opal.controllers').controller('DeleteFormCtrl', function($scope, $modal){
  /*
  * Allows the user to open a delete episode confirmation modal.
  * If they choose to delete we delete the episode and
  * redirect to patient detail page.
  */
  "use strict";
  var episode = $scope.pathway.episode;
  $scope.delete = function(){
    $modal.open({
      templateUrl: '/templates/delete_modal.html',
      controller: ['$scope', '$modalInstance', function ($scope, $modalInstance) {
        $scope.episode = episode
        $scope.deleteUrl = "/delete-episode/" +  episode.demographics[0].patient_id + "/" + episode.id + "/";
        $scope.cancel = function() {
          $modalInstance.close('cancel');
        };
      }],
    });
  }
});