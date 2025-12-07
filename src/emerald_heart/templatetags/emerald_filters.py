from __future__ import annotations

import logging

from django import template
from django.conf import settings
from django.utils.safestring import SafeString, SafeText, mark_safe

LOG = logging.getLogger(__name__)

register = template.Library()


@register.filter(name="addclass")
def addclass(value: object, arg: str):
    """Add a css class to a bound form."""
    try:
        return value.as_widget(attrs={"class": arg})  # type: ignore
    except Exception:
        if isinstance(value, (str, SafeString, SafeText)):
            if 'class="' in value:
                return mark_safe(value.replace('class="', f'class="{arg} '))
            elif "class='" in value:
                return mark_safe(value.replace("class='", f"class='{arg} "))
            elif "<label for=" in value:
                return mark_safe(value.replace("<label for=", f'<label class="{arg}" for='))

        LOG.exception("Unable to add class `%s` to `%s`. %s", arg, value, value.__module__)
        return value


@register.filter(name="display_name")
def display_name(data: object) -> str:
    """Return the data's display value if the attribute is present."""
    try:
        return data.display_name  # type: ignore
    except Exception:
        return str(data)


@register.filter(name="item_type")
def item_type(data: object) -> str:
    """Return the object type as a string value."""
    return type(data).__name__


@register.filter("startswith")
def startswith(value: object, arg: str) -> bool:
    """Check if a value starts with a given substring (case sensitive)."""
    if isinstance(value, str):
        return value.startswith(arg)
    return False


@register.filter("istartswith")
def istartswith(value: object, arg: str) -> bool:
    """Check if a value starts with a given substring (case insensitive)."""
    if isinstance(value, str) and isinstance(arg, str):
        return value.lower().startswith(arg.lower())
    return False


@register.filter(is_safe=False)
def default_if_unset(value: object, arg: object) -> object:
    """If value is falsey, use given default."""
    invalid_string = getattr(settings, "string_if_invalid", "")
    if not value or value is None or value == "" or value == invalid_string:
        return arg
    return value
