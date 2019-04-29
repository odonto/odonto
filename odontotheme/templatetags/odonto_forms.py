"""
Templatetags for form/modal helpers
"""
from django import template
from opal.templatetags.forms import extract_common_args

register = template.Library()


@register.inclusion_tag('_helpers/btn_checkbox.html')
def btn_checkbox(*args, **kwargs):
    """
    Render a text input

    Kwargs:
    - hide : Condition to hide
    - show : Condition to show
    - model: Angular model
    - label: User visible label
    - lookuplist: Name of the lookuplist
    - required: label to show when we're required!
    """
    return extract_common_args(kwargs)



@register.inclusion_tag('_helpers/btn_radio.html')
def btn_radio(*args, **kwargs):
    return extract_common_args(kwargs)


def extract_numeric_args(kwargs):
    ctx = extract_common_args(kwargs)
    numeric_args = [
        "min", "max"
    ]

    for i in numeric_args:
        if i in kwargs:
            ctx[i] = kwargs.pop(i)
    return ctx


@register.inclusion_tag('_helpers/number.html')
def number(*args, **kwargs):
    ctx = extract_numeric_args(kwargs)
    ctx["style"] = "vertical"
    return ctx

@register.inclusion_tag('_helpers/number.html')
def teeth(*args, **kwargs):
    ctx = extract_numeric_args(kwargs)
    ctx.setdefault("min", 0)
    ctx.setdefault("max", 50)
    ctx["style"] = "vertical"
    return ctx


