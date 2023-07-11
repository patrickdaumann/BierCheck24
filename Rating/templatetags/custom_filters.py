from django import template
import os

register = template.Library()

@register.filter
def file_exists(filepath):
    return os.path.isfile(filepath)


#wird momentan nicht verwendet