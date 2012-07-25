from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.contrib.auth.decorators import login_required

from home.views import HomeView, LogOutView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'', include('social_auth.urls')),

    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^logout/$', login_required(LogOutView.as_view()), name='logout'),
    url(r'^entries/', include('entries.urls', namespace='entries')),
    url(r'^profiles/', include('profiles.urls', namespace='profiles')),

    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    )
