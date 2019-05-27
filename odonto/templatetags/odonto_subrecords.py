"""
Odonto Subrecord rendering
"""
from django import template
from opal.models import PatientSubrecord

register = template.Library()

@register.inclusion_tag('templatetags/subrecord.html', takes_context=True)
def subrecord(context, model):
    """
    Templatetag to render our subrecord display templates.
    """
    episode = context['object']
    model_class = model.__class__

    if issubclass(model_class, PatientSubrecord):
        object_list = model_class.objects.filter(patient=episode.patient)
    else:
        object_list = model_class.objects.filter(episode=episode)

    return {
        'display_template_name': model.get_display_template(),
        'object_list'          : object_list
    }


@register.inclusion_tag('templatetags/subrecord_row.html', takes_context=True)
def subrecord_row(context, model):
    return {
        'object': context['object'],
        'model' : model
    }
