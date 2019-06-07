from django.contrib import admin
from reversion.admin import VersionAdmin
from odonto import models

admin.site.register(models.Performer, VersionAdmin)