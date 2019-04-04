"""
Templatetags to help with display
"""
from django import template

register = template.Library()

@register.inclusion_tag('_helpers/render_field')
def render_field():
    return {}
