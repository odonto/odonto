angular.module('opal.controllers').controller(
  'CareProviderStepCtrl',
  function(scope, step, episode){
  scope.editing.fp17_dental_care_provider.provider_name = 'Northumbria HCT';
  //    scope.editing.fp17_dental_care_provider.provider_location_number = '327836287';
  scope.editing.fp17_dental_care_provider.provider_address = "Albion Road Clinic\nAlbion Road\nNorth Shields\nNE29 0HG";
  if(scope.metadata.performer.current_user){
      scope.editing.fp17_dental_care_provider.performer = scope.metadata.performer.current_user;
  }
});
