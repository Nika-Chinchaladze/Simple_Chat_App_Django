from django import template
from chat_app.models import Message

register = template.Library()


@register.filter(name="check")
def check(value):
    if value is not None:
        return True
    return False


@register.filter(name="find_name")
def find_name(value):
    my_user = Message.objects.filter(id=int(value)).first()
    return my_user.username
