from django import template

from antsWeb.ants_admin.models import ConfigEntry

register = template.Library()


@register.filter(name='get_settings')
def get_settings(name):
    try:
        entry = ConfigEntry.objects.get(name=name)
        return entry.value
    except ConfigEntry.DoesNotExist:
        return ''
