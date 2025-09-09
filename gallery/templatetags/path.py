from django import template
from os.path import join

from django.template.defaultfilters import safe

from config.settings import MEDIA_URL

register = template.Library()


@register.simple_tag
def get_url_picture(data):
    if data:
        return safe(join(MEDIA_URL, str(data)))
    return ''
