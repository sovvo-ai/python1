from django import template
from django.utils.html import strip_tags

register = template.Library()

@register.filter
def reading_time(content):
    text = strip_tags( content)
    minutes = len(text) // 300
    if minutes ==0:
        return '不到1分钟'
    return f'约{minutes}分钟'

@register.filter
def first_sentence(value):
    text = strip_tags(value)
    parts = text.split('。')
    return parts[0] + '。' if len( parts) > 1 else text
