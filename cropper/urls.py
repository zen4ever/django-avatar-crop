from django.conf.urls.defaults import *

urlpatterns = patterns('cropper.views',
    url(r'^avatar_upload/$', 'avatar_upload', name='cropper_avatar_upload'),
    url(r'^avatar_crop/$', 'avatar_crop', name='cropper_avatar_crop'),
)
