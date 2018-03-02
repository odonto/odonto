from opal.core import pathway
from odonto import models


class AddPatientPathway(pathway.PagePathway):
    display_name = "Add Patient"
    slug = "add_patient"
    steps = (
        models.Demographics,
    )

class Fp17Pathway(pathway.PagePathway):
    display_name = 'FP17 Claim Form'
    slug = 'fp17'
    steps = (
        pathway.Step(
            model=models.Demographics,
            display_name='Demographics',
            ),
        pathway.Step(
            model=models.Fp17DentalCareProvider,
            display_name="Care Provider"),
        pathway.Step(
            model=models.Fp17IncompleteTreatment,
            display_name="Incomplete Treatment and Treatment Dates"),
        pathway.Step(
            model=models.Fp17Exemptions,
            display_name="Exemptions and Remissions"),
        pathway.Step(
            model=models.Fp17TreatmentCategory,
            display_name="Treatment Category"),
        pathway.Step(
            model=models.Fp17ClinicalDataSet,
            display_name="Clinical Data Set"),
        pathway.Step(
            model=models.Fp17OtherDentalServices,
            display_name="Other Services"),
        pathway.Step(
            model=models.Fp17Recall,
            display_name="NICE Guidance"),
        pathway.Step(
            model=models.Fp17NHSBSAFields,
            display_name="NHS BSA Use Only"),
        pathway.Step(
            model=models.Fp17Declaration,
            display_name="Declaration"),
    )
