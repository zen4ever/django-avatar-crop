from django.conf.urls.defaults import *

urlpatterns = patterns('avatar_crop.views',
    url(r'^crop/(\d+)/$', 'avatar_crop', name='avatar_crop'),
    url(r'^crop/$', 'avatar_crop', name='avatar_crop_default'),
)
