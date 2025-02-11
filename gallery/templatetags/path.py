from django import template
from  os.path import join

from config.settings import MEDIA_URL

register = template.Library()


@register.simple_tag
def get_url_picture(data):
    return join(MEDIA_URL, str(data))