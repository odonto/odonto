describe('CovidTriageDateTimeOfContact', function() {
  "use strict";
  var CovidTriageDateTimeOfContact;
  var editing;
  var step;

  beforeEach(module('opal.filters'));
  beforeEach(module('opal.services'));

  beforeEach(function(){
      inject(function($injector){
        CovidTriageDateTimeOfContact  = $injector.get('CovidTriageDateTimeOfContact');
      });
      editing = {covid_triage: {}};
      step = {other_triage: []}
  });

  describe('datetime of contact should be required', function(){
    it('should error if there is no time of contact', function(){
      var result = CovidTriageDateTimeOfContact(editing, step);
      expect(result).toEqual({
        covid_triage: {
          datetime_of_contact: "Date/time of contact is required"
        }
      });
    });

    it('should not if there is a time of contact', function(){
      editing.covid_triage.datetime_of_contact = new Date();
      var result = CovidTriageDateTimeOfContact(editing, step);
      expect(result).toBeUndefined();
    });
  });

  describe('datetime of contact should not be the same as a different triage', function(){
    it('should error if there is a triage with the same date', function(){
      editing.covid_triage.datetime_of_contact = new Date(2020, 4, 21, 12, 40);
      step.other_triage = ["21/05/2020 12:40:00"]
      var result = CovidTriageDateTimeOfContact(editing, step);
      expect(result).toEqual({
        covid_triage: {
          datetime_of_contact: "Date/time of contact matches a previously submitted triage claim"
        }
      });
    });

    it('should not error if there is a triage with the different date', function(){
      editing.covid_triage.datetime_of_contact = new Date(2020, 2, 22, 13, 40);
      step.other_triage = ["21/03/2020 12:40:00"]
      var result = CovidTriageDateTimeOfContact(editing, step);
      expect(result).toBeUndefined();
    });
  });
});


