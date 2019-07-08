from django.contrib import admin
from reversion.admin import VersionAdmin
from . import models

admin.site.register(models.SystemClaim, VersionAdmin)
admin.site.register(models.Submission, VersionAdmin)
admin.site.register(models.BCDS1Message, VersionAdmin)