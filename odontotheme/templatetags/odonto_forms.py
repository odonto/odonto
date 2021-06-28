"""
Templatetags for form/modal helpers
"""
from django import template
from opal.templatetags.forms import (
    extract_common_args, _input, _model_and_field_from_path
)
from opal.core.subrecords import get_subrecord_from_model_name

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
    result = get_odonto_common_args(kwargs)
    result["label_size"] = kwargs.get("field_size", 9)
    result["field_size"] = kwargs.get("field_size", 12-result["label_size"])
    return result


@register.inclusion_tag('_helpers/btn_radio.html')
def btn_radio(*args, **kwargs):
    ctx = get_odonto_common_args(kwargs)
    popover_template = kwargs.get("popover_template")
    if popover_template:
        ctx["popover_template"] = popover_template
    return ctx


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
    ctx["unit"] = kwargs.get("unit")
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
    if "style" not in kwargs:
        context["style"] = "vertical"
    if 'mindate' in kwargs:
        context['mindate'] = kwargs['mindate']
    context["user_options"] = kwargs.pop("user_options", False)
    return context


@register.inclusion_tag('_helpers/extraction_chart.html')
def extraction_chart(*args, **kwargs):
    ctx = {}
    return ctx


@register.inclusion_tag('_helpers/chart_tooth.html')
def chart_tooth(notation, **kwargs):
    """
    Displays a box which can be used as part of a dental chart
    """
    label_value = notation[2:]
    label = kwargs.pop("label", True)
    label_position = 'below'

    if notation[1].lower == 'l':
        try:
            int(notation[1:])
            label = False  # We don't label lower permanent
        except Exception:
            # Lower deciduous are labelled below
            label_position = 'above'

    model = "editing.{0}.{1}".format(
        get_subrecord_from_model_name('ExtractionChart').get_api_name(),
        "{0}_{1}".format(notation[:2], label_value).lower()
    )

    ctx = {
        'notation'      : notation,
        'label'         : label,
        'label_value'   : label_value,
        'label_position': label_position,
        'model'         : model
    }
    return ctx


@register.inclusion_tag('_helpers/odonto_select.html')
def odonto_select(*args, **kwargs):
    ctx = get_odonto_common_args(kwargs)
    ctx['lookuplist'] = kwargs.pop("lookuplist", ctx.get("lookuplist", None))
    ctx["directives"] = args
    return ctx


@register.inclusion_tag('_helpers/odonto_datetime_picker.html')
def odonto_datetimepicker(*args, **kwargs):
    ctx = get_odonto_common_args(kwargs)
    ctx["field"] = kwargs["field"]
    return ctx
