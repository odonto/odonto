from opal.core import pathway
from openodonto import models


class Fp17Pathway(pathway.PagePathway):
    display_name = 'FP17 Claim Form'
    slug = 'fp17'
    steps = (
        models.Demographics,
        models.Fp17DentalCareProvider,
        models.Fp17IncompleteTreatment,
        models.Fp17Exemptions,
        models.Fp17TreatmentCategory,
        models.Fp17ClinicalDataSet,
        models.Fp17OtherDentalServices,
        models.Fp17Recall,
        models.Fp17NHSBSAFields,
        models.Fp17Declaration,
    )
