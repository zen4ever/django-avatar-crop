from django.conf import settings
AVATAR_CROP_MAX_SIZE = getattr(settings, 'AVATAR_CROP_MAX_SIZE', 450)
AVATAR_CROP_MIN_SIZE = getattr(settings, 'AVATAR_CROP_MIN_SIZE', 49)
