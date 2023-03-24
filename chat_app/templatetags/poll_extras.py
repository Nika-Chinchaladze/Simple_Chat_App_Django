from django import template

register = template.Library()


@register.filter(name="check")
def check(value):
    if value is not None:
        return True
    return False