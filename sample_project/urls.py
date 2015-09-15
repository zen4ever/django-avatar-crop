from django.conf.urls import url, patterns, include
from django.views.generic.base import RedirectView

from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^avatar/', include('avatar.urls')),
    url(r'^avatar_crop/', include('avatar_crop.urls')),
    url(r'^accounts/login/', 'django.contrib.auth.views.login', name='auth_login'),
    url(r'^accounts/logout/', 'django.contrib.auth.views.logout', name='auth_logout'),
    url(r'^$', RedirectView.as_view(url='/avatar/change/')),
)

from django.conf import settings

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += patterns('', (
        r'^site_media/media/(?P<path>.*)$',
        'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}
        ),
    ) 
