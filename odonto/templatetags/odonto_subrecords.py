"""
Odonto Subrecord rendering
"""
from django import template

register = template.Library()


@register.inclusion_tag('templatetags/subrecord_row.html', takes_context=True)
def subrecord_row(context, model, object_list=None, pathway=None):
    if not object_list:
        if pathway:
            object_list = "editing.{}".format(model.get_api_name())
            if model._is_singleton:
                object_list = "[{}]".format(object_list)
        else:
            object_list = "episode.{}".format(model.get_api_name())
    return {
        'model': model,
        'object_list': object_list
    }
