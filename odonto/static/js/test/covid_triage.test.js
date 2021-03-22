describe('CovidTriageTimeOfContact', function() {
  "use strict";
  var CovidTriageTimeOfContact;
  var editing;
  var step;

  beforeEach(module('opal.filters'));
  beforeEach(module('opal.services'));

  beforeEach(function(){
      inject(function($injector){
        CovidTriageTimeOfContact  = $injector.get('CovidTriageTimeOfContact');
      });
      editing = {covid_triage: {}};
      step = {other_triage: []}
  });

  describe('time of contact should be required', function(){
    it('should error if there is no time of contact', function(){
      var result = CovidTriageTimeOfContact(editing, step);
      expect(result).toEqual({
        covid_triage: {
          time_of_contact: "Time of contact is required"
        }
      });
    });

    it('should not if there is a time of contact', function(){
      editing.covid_triage.time_of_contact = new Date();
      var result = CovidTriageTimeOfContact(editing, step);
      expect(result).toBeUndefined();
    });
  });

  describe('time of contact should not be the same as a different triage', function(){
    it('should error if there is a triage with the same date', function(){
      editing.covid_triage.date_of_contact = new Date(2020, 4, 21);
      editing.covid_triage.time_of_contact = "12:40:00";
      step.other_triage = ["21/05/2020 12:40:00"]
      var result = CovidTriageTimeOfContact(editing, step);
      expect(result).toEqual({
        covid_triage: {
          time_of_contact: "Date/time of contact matches a previously submitted triage claim"
        }
      });
    });

    it('should not error if there is a triage with the different date', function(){
      editing.covid_triage.date_of_contact = new Date(2020, 2, 22);
      editing.covid_triage.time_of_contact = "13:40:00";
      step.other_triage = ["21/03/2020 12:40:00"]
      var result = CovidTriageTimeOfContact(editing, step);
      expect(result).toBeUndefined();
    });

    it('should not error if there is no triage date', function(){
      editing.covid_triage.time_of_contact = "11:30:00";
      var result = CovidTriageTimeOfContact(editing, step);
      expect(result).toBeUndefined();
    });
  });
});


