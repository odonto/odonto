describe("CaseMixHelper", function () {
  "use strict";
  var editing, step, Fp17FreeRepairAllowed, expectedError;
  beforeEach(module('opal.filters'));
  beforeEach(module('opal.services'));

  beforeEach(function () {
    inject(function ($injector) {
      Fp17FreeRepairAllowed = $injector.get("Fp17FreeRepairAllowed");
    });
    editing = {
      fp17_other_dental_services: {
        free_repair_or_replacement: true,
      },
      fp17_incomplete_treatment: {
        completion_or_last_visit: "03/02/2020",
      },
      fp17_treatment_category: {
        treatment_category: "Band 3",
      },
    };
    step = {
      submitted_bands: [["03/01/2020", "Band 1"]],
    };
    expectedError = {
      fp17_other_dental_services: {
        free_repair_or_replacement:
          "No previous guarenteed item for this patient",
      },
    };
  });

  it("should not error if it not free repair or replacement", function () {
    editing.fp17_other_dental_services.free_repair_or_replacement = false;
    expect(Fp17FreeRepairAllowed(editing, step)).toBeUndefined();
  });

  it("should not error if there is no completion or last visit", function () {
    editing.fp17_incomplete_treatment.completion_or_last_visit = null;
    expect(Fp17FreeRepairAllowed(editing, step)).toBeUndefined();
  });

  it("should not error if there is an equal band within the last 12 months", function () {
    step.submitted_bands = [["03/01/2020", "Band 3"]];
    expect(Fp17FreeRepairAllowed(editing, step)).toBeUndefined();
  });

  it("should not error if there is an higher band within the last 12 months", function () {
    step.submitted_bands = [["03/01/2020", "Band 3"]];
    editing.fp17_treatment_category.treatment_category = "Band 1";
    expect(Fp17FreeRepairAllowed(editing, step)).toBeUndefined();
  });

  it("should error if there are no previous submissions", function () {
    step.submitted_bands = [];
    editing.fp17_treatment_category.treatment_category = "Band 1";
    expect(Fp17FreeRepairAllowed(editing, step)).toEqual(expectedError);
  });

  it("should error if there are no previous submissions with a higher band", function () {
    step.submitted_bands = [["03/01/2020", "Band 1"]];
    expect(Fp17FreeRepairAllowed(editing, step)).toEqual(expectedError);
  });

  it("should error if it is not an appropriate category", function () {
    editing.fp17_treatment_category.treatment_category = "Arrest of bleeding";
    expectedError = {
      fp17_other_dental_services: {
        free_repair_or_replacement:
        "Inappropriate treatment category for a free repair",
      },
    };
    expect(Fp17FreeRepairAllowed(editing, step)).toEqual(expectedError);
  });
});
