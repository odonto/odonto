"""
Odonto Link templatetags
"""
from django import template

register = template.Library()

@register.inclusion_tag('templatetags/links/link_to.html')
def link_to(link_text, target, **kwargs):
    return dict(
        href=target.get_absolute_url(**kwargs),
        link_text=link_text
    )
