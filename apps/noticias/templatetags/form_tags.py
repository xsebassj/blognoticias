from django import template
from django.forms.boundfield import BoundField

register = template.Library()

@register.filter(name='add_class')
def add_class(value, css_class):
    if isinstance(value, BoundField):
        return value.as_widget(attrs={"class": css_class})
    return value
@register.filter(name='add_error_class')
def add_error_class(field):
    css_class = "form-control"
    if field.errors:
        css_class += " is-invalid"
    return field.as_widget(attrs={"class": css_class})