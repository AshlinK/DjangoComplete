from django import template
register=template.Library()

def upper(value):
    return value.upper()

register.filter('upper',upper)