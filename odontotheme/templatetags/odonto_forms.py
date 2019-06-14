"""
Templatetags for form/modal helpers
"""
from django import template
from opal.templatetags.forms import (
    extract_common_args, _input, _model_and_field_from_path
)

register = template.Library()


def get_odonto_common_args(kwargs):
    ctx = extract_common_args(kwargs)
    api_name, field_name = get_field_name_and_api_name(kwargs["field"])
    ctx["model_api_name"] = api_name
    ctx["field_name"] = field_name
    return ctx


def get_field_name_and_api_name(subrecord_field_path):
    """
    returns the field and the api name for the context
    """
    _, field_name = subrecord_field_path.split('.')
    model, field = _model_and_field_from_path(subrecord_field_path)
    return model.get_api_name(), field_name


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
    return get_odonto_common_args(kwargs)



@register.inclusion_tag('_helpers/btn_radio.html')
def btn_radio(*args, **kwargs):
    return get_odonto_common_args(kwargs)


def extract_numeric_args(kwargs):
    ctx = get_odonto_common_args(kwargs)
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


@register.inclusion_tag('_helpers/char_field.html')
def charfield(*args, **kwargs):
    """
    Similar to the input field in opal but accepts
    pattern and min length
    and is always vertical
    """
    ctx = _input(*args, **kwargs)
    ctx["style"] = "vertical"
    api_name, field_name = get_field_name_and_api_name(kwargs["field"])
    ctx["model_api_name"] = api_name
    ctx["field_name"] = field_name

    if "pattern" not in kwargs and "pattern_error" in kwargs:
        raise ValueError("Pattern error passed in but no pattern")

    for field in ["pattern", "minlength", "pattern_error"]:
        if field in kwargs:
            ctx[field] = kwargs[field]
    return ctx


@register.inclusion_tag('_helpers/datepicker.html')
def odonto_datepicker(*args, **kwargs):
    kwargs["datepicker"] = True
    context = _input(*args, **kwargs)
    api_name, field_name = get_field_name_and_api_name(kwargs["field"])
    context["model_api_name"] = api_name
    context["field_name"] = field_name
    if 'mindate' in kwargs:
        context['mindate'] = kwargs['mindate']
    context["user_options"] = kwargs.pop("user_options", False)
    return context

