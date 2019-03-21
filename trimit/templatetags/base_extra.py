from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='is_hairdresser')
def is_hairdresser(user):
    group = Group.objects.get(name='hairdressers')
    return True if group in user.groups.all() else False