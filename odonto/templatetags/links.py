"""
Odonto Link templatetags
"""
from django.urls import reverse
from django import template
import six

register = template.Library()


def _link_url(target, **kwargs):
    if isinstance(target, six.string_types):
        if 'ngpk' in kwargs:
            ngpk = kwargs.pop('ngpk')
            base = reverse(target, kwargs=kwargs)
            return '{0}{1}/'.format(base, ngpk)
        else:
            return reverse(target, kwargs=kwargs)
    return target.get_absolute_url(**kwargs)

def build_link_context(link_text, target, **kwargs):
    """
    Return a dict of common link template context.

    * href
    * link_text
    * classes
    """
    context = {}
    if 'classes' in kwargs:
        context['classes'] = kwargs.pop('classes')
    else:
        context['classes'] = ''

    context['href'] = _link_url(target, **kwargs)
    context['link_text'] = link_text

    return context

@register.simple_tag
def link_url(target, **kwargs):
    return _link_url(target, **kwargs)

@register.inclusion_tag('templatetags/links/link_to.html')
def link_to(link_text, target, **kwargs):
    """
    Render a link to TARGET displaying TEXT
    If TARGET is a stringlike thing, we assume it to be a named url
    and look it up with `reverse()`

    Add supplementary classes to the link with the kwarg `classes`

    We pass remaining kwargs to `get_absolute_url()` or `reverse()`.
    """
    return build_link_context(link_text, target, **kwargs)


@register.inclusion_tag('templatetags/links/link_to.html')
def button_to(link_text, target, **kwargs):
    """
    Render a button to TARGET displaying TEXT.
    If TARGET is a stringlike thing, we assume it to be a named url
    and look it up with `reverse()`

    Add an icon prefix with the kwarg `icon`.
    Add supplementary classes to the link with the kwarg `classes`

    We pass remaining kwargs to `get_absolute_url()` or `reverse()`.
    """
    iconname = None
    if 'icon' in kwargs:
        iconname = kwargs.pop('icon')

    context = build_link_context(link_text, target, **kwargs)

    if iconname:
        context['iconname'] = iconname

    context['classes'] = 'btn {0}'.format(context['classes'])
    return context
