from django.conf import settings
AVATAR_CROP_MAX_SIZE = getattr(settings, 'AVATAR_CROP_MAX_SIZE', 450)
