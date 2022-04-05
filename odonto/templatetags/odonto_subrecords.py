"""
Odonto Subrecord rendering
"""
from django import template
from opal.templatetags import forms
from django.db import models
from odonto.models import CovidStatus

register = template.Library()


@register.inclusion_tag('templatetags/subrecord_row.html', takes_context=True)
def subrecord_row(context, model, object_list=None, pathway=None, title=None):
    if not object_list:
        if pathway:
            object_list = "editing.{}".format(model.get_api_name())
            if model._is_singleton:
                object_list = "[{}]".format(object_list)
        else:
            object_list = "episode.{}".format(model.get_api_name())
    if not title:
        title = model.get_display_name()
    return {
        'model': model,
        'object_list': object_list,
        'title': title,
        'pathway': pathway
    }


@register.inclusion_tag('templatetags/table_row_field_display.html')
def table_row_field_display(model_and_field):
    model, field = forms._model_and_field_from_path(model_and_field)
    ctx = {
        "model": "item.{}".format(field.attname),
        "display_name": model._get_field_title(field.attname),
    }
    if isinstance(field, (models.BooleanField, models.NullBooleanField,)):
        ctx["is_boolean"] = True
    if isinstance(field, models.DateField):
        ctx["is_date"] = True
    if isinstance(field, models.TimeField):
        ctx["is_time"] = True
    return ctx


@register.inclusion_tag('templatetags/covid_status_row_display.html')
def covid_status_row_display(field):
    """
    Displays a patient's covid status in a table.
    """
    ctx = {
        "model": "item.{}".format(field),
        "display_name": CovidStatus._get_field_title(field),
    }
    return ctx
