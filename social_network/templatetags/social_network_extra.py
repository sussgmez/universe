from django import template
from ..models import Profile, Post

register = template.Library()

@register.filter
def get_likes(value):
    return len(Profile.objects.filter(liked_post=value))
    
@register.filter
def get_comments(value):
    return len(Post.objects.filter(commented=value))
    
@register.filter
def get_followers(value):
    return len(Profile.objects.filter(following=value)) - 1
