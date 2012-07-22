from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

from home.views import HomeView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='home'),

    url(r'^social/', include('socialregistration.urls', namespace = 'socialregistration')),
    url(r'^admin/', include(admin.site.urls)),
)
