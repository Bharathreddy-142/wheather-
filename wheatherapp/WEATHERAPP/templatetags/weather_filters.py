from django import template
from datetime import datetime

register = template.Library()


@register.filter
def dict_lookup(dictionary, key):
    """
    Custom filter to lookup values in a dictionary in templates
    Usage: {{ dictionary|dict_lookup:key }}
    """
    if dictionary is None:
        return None
    return dictionary.get(key)


@register.filter
def unix_to_time(unix_timestamp):
    """
    Convert Unix timestamp to time format
    Usage: {{ timestamp|unix_to_time }}
    """
    if not unix_timestamp:
        return "N/A"
    try:
        return datetime.fromtimestamp(unix_timestamp).strftime('%H:%M')
    except (ValueError, TypeError, OSError):
        return "N/A"

