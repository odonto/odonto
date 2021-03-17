(function(){
  var app = angular.module('opal');
  app.controller('WelcomeCtrl', function(){});

  app.config(
      ['$routeProvider',
       function($routeProvider){
           $routeProvider.when('/',  {
               controller: 'WelcomeCtrl',
               templateUrl: '/templates/welcome.html'}
           ),
           $routeProvider.when('/patient/',  {
            controller: 'WelcomeCtrl',
            templateUrl: '/templates/welcome.html'}
        )
        .when('/summary/fp17/:patient_id/:episode_id', {
          controller: 'SummaryCtrl',
                resolve: {
                    patient: function(patientLoader) { return patientLoader(); },
                },
          templateUrl: function(params){ return '/templates/view_summary_fp17.html' }
        })
        .when('/summary/fp17o/:patient_id/:episode_id', {
          controller: 'SummaryCtrl',
                resolve: {
                    patient: function(patientLoader) { return patientLoader(); },
                },
          templateUrl: function(params){ return '/templates/view_summary_fp17o.html' }
        })
        .when('/summary/covid-triage/:patient_id/:episode_id', {
          controller: 'SummaryCtrl',
                resolve: {
                    patient: function(patientLoader) { return patientLoader(); },
                },
          templateUrl: function(params){ return '/templates/view_summary_covid_triage.html' }
        })
       }]);
})();
