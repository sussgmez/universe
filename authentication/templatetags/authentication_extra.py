from django import template
from ..models import Profile
from django.utils import timezone
from datetime import datetime

register = template.Library()

@register.filter
def get_likes(value):
    return len(Profile.objects.filter(liked_publications=value))
     
@register.filter
def get_followers(value):
    return len(Profile.objects.filter(following=value)) - 1
