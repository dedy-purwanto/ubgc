from django.conf.urls.defaults import patterns, url

from .views import DetailView, UpdateView

urlpatterns = patterns('',
    url(r'^(?P<pk>\d+)/$', DetailView.as_view(), name='detail'),
    url(r'^update/$', UpdateView.as_view(), name='update'),
)
