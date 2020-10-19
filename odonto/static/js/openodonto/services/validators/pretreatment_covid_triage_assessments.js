angular.module('opal.services').factory('PretreatmentCovidTriageAssessments', function(){
  return function(editing, step){
    "use strict";
    if(editing.pretreatment_covid_triage_assessments.number_of_assessments){
      if(!editing.pretreatment_covid_triage_assessments.triage_type){
        return {
          "pretreatment_covid_triage_assessments": {
            "number_of_assessments": 'There cannot be a number of assessments but no triage type'
          }
        }
      }
    }
  }
});