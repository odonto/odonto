from django.contrib import admin
from django.contrib.auth.models import User
from reversion.admin import VersionAdmin
from odonto import models
from opal.admin import UserProfileAdmin


class HasEthnicity(admin.SimpleListFilter):
    title = 'Ethnicity'

    parameter_name = 'has_ethnicity'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('ethnicity_populated', 'Has ethnicity'),
            ('ethnicity_not_populated', 'Does not have ethnicity'),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value() == 'ethnicity_populated':
            return queryset.exclude(
                ethnicity_fk_id=None
            )
        if self.value() == 'ethnicity_not_populated':
            return queryset.filter(
                ethnicity_fk_id=None
            )


class DemographicsAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'surname', 'date_of_birth', 'ethnicity_fk')
    list_filter = (HasEthnicity,)
    list_editable = ("ethnicity_fk",)


class PerformerNumberAdmin(VersionAdmin):
    list_display = ('user', 'number', 'dpb_pin')


user_admin_list_display = list(UserProfileAdmin.list_display)
user_admin_list_display.append("dpb_pin")


class OdontoUserAdmin(UserProfileAdmin):
    list_display = user_admin_list_display

    def dpb_pin(self, obj):
        if obj.performernumber_set.count() > 0:
            return obj.performernumber_set.get().dpb_pin
        return ''

admin.site.unregister(models.Demographics)
admin.site.register(models.Demographics, DemographicsAdmin)
admin.site.register(models.PerformerNumber, PerformerNumberAdmin)
admin.site.unregister(User)
admin.site.register(User, OdontoUserAdmin)
