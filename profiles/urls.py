from django.conf.urls.defaults import *

urlpatterns = patterns('profiles.views',
    url(r'^avatar_upload/$', 'avatar_upload', name='profiles_avatar_upload'),
    url(r'^avatar_crop/$', 'avatar_crop', name='profiles_avatar_crop'),
)
