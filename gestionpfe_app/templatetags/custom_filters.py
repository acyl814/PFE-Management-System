from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='break_lines')
def break_lines(value, word_count=7):
    words = value.split()
    lines = [' '.join(words[i:i + word_count]) for i in range(0, len(words), word_count)]
    return mark_safe('<br>'.join(lines))