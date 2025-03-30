from django import template
from ..models import Publication
from django.utils import timezone
from datetime import datetime

register = template.Library()

@register.filter
def get_comments(value):
    return len(Publication.objects.filter(commented=value))

@register.filter
def format_date(date):
    now = timezone.now()
    df = now - date
    if (df.days < 1):
        if (df.seconds//60 < 1): return f'{df.seconds//1}s'
        elif (df.seconds//60 < 60): return f'{df.seconds//60}min' 
        else: return f'{df.seconds//3600}h'
    elif (df.days < 5): return f'{df.days}d'

    else: return f'{datetime.strftime(date, "%d/%m/%Y")}'

@register.filter
def get_category_num(category):
    num = len(Publication.objects.filter(category=category))
    return num
