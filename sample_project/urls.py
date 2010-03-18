from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^profilecrop/', include('profilecrop.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/(.*)', admin.site.root),
    (r'^avatar/', include('avatar.urls')),
    (r'^avatar_crop/', include('avatar_crop.urls')),
    url(r'^accounts/login/', 'django.contrib.auth.views.login', name='auth_login'),
    url(r'^accounts/logout/', 'django.contrib.auth.views.logout', name='auth_logout'),
    url(r'^$', 'django.views.generic.simple.redirect_to', {'url': '/avatar/change/'}),
)

from django.conf import settings
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'', include('staticfiles.urls')),
    )
