from django import template
import re

register = template.Library()

@register.filter
def duration(seconds):
    if not seconds:
        return ''
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes}:{secs:02d}"

@register.filter
def clean_description(value):
    if not value:
        return ''
    """
    Remove the "Read more on Last.fm" link and everything after it
    """
    cleaned = re.sub(r'<a href="[^"]*">Read more on Last\.fm</a>\.?', '', value)
    """
    Strip any remaining HTML tags
    """
    cleaned = re.sub(r'<[^>]+>', '', cleaned)
    return cleaned.strip()