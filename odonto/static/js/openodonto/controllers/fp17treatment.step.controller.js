angular.module('opal.controllers').controller('FP17TreatmentStepCtrl', function(scope, step, episode){

    //
    // Set up defaults
    //
    if(!scope.editing.fp17_incomplete_treatment.date_of_acceptance){
        scope.editing.fp17_incomplete_treatment.date_of_acceptance = new Date();
    }


});
