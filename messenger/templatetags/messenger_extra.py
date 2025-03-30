from django import template
from django.utils import timezone
from datetime import datetime

register = template.Library()

@register.filter
def get_chat_name(chat, user):
    names = []
    for profile in chat.profiles.all():
        if profile != user.profile: names.append(profile.user.get_full_name())
    return ', '.join(names)

@register.filter
def get_chat_description(chat, user):
    usernames = []
    for profile in chat.profiles.all():
        if profile != user.profile: usernames.append(f'@{profile.user.username}')
    return ', '.join(usernames)

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
