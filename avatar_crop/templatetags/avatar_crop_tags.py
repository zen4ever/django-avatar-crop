from django import template
register = template.Library()

def avatar_crop_url(avatar, size=80):
    if not avatar.thumbnail_exists(size):
        avatar.create_thumbnail(size)
    return avatar.avatar_url(size)
register.simple_tag(avatar_crop_url)
