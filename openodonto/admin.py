from django.contrib import admin
from openodonto import models


admin.site.register(models.Fp17DentalCareProvider)
admin.site.register(models.Fp17IncompleteTreatment)
admin.site.register(models.Fp17Exemptions)
admin.site.register(models.Fp17TreatmentCategory)
admin.site.register(models.Fp17ClinicalDataSet)
admin.site.register(models.Fp17OtherDentalServices)
admin.site.register(models.Fp17Recall)
admin.site.register(models.Fp17NHSBSAFields)
admin.site.register(models.Fp17Declaration)
