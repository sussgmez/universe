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

@register.filter
def get_100_messages(messages):
    return messages.order_by('-created')[:100]


@register.filter
def get_chat_name(chat, user):
    names = []
    for profile in chat.profiles.all():
        if profile != user.profile: names.append(profile.user.get_full_name())
    return ', '.join(names)


@register.filter
def get_chat_image(chat, user):
    profiles = chat.profiles.all()

    if len(profiles) <= 2:
        for profile in profiles:
            if profile != user.profile:
                if profile.image:
                    return profile.image.url
                else:
                    return '/static/images/no-profile.png'
    else:
        return '/static/images/group.png'