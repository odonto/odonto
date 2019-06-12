"""
Templatetags for form/modal helpers
"""
from django import template
from opal.templatetags.forms import extract_common_args, _input
from opal.core.subrecords import get_subrecord_from_model_name

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


@register.inclusion_tag('_helpers/char_field.html')
def charfield(*args, **kwargs):
    """
    Similar to the input field in opal but accepts
    pattern and min length
    and is always vertical
    """
    ctx = _input(*args, **kwargs)
    ctx["style"] = "vertical"

    if "pattern" not in kwargs and "pattern_error" in kwargs:
        raise ValueError("Pattern error passed in but no pattern")

    for field in ["pattern", "minlength", "pattern_error"]:
        if field in kwargs:
            ctx[field] = kwargs[field]
    return ctx


@register.inclusion_tag('_helpers/extraction_chart.html')
def extraction_chart(*args, **kwargs):
    ctx = {}
    return ctx


@register.inclusion_tag('_helpers/chart_tooth.html')
def chart_tooth(notation, **kwargs):
    """
    Displays a box which can be used as part of a dental chart
    """
    label_value    = notation[2:]
    label          = True
    label_position = 'below'

    if notation[1].lower == 'l':
        try:
            int(notation[1:])
            label = False # We don't label lower permanent
        except:
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
