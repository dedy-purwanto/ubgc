from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required

from .views import CreateView, UpdateView, DetailView, VoteCreateView

urlpatterns = patterns('',
    url(r'^(?P<pk>\d+)/edit/$', login_required(UpdateView.as_view()), name='edit'),
    url(r'^(?P<pk>\d+)/vote/$', login_required(VoteCreateView.as_view()), name='vote'),
    url(r'^(?P<pk>\d+)/play/(?P<slug>[-\w]+)/$', DetailView.as_view(), name='play'),
    url(r'^new/$', login_required(CreateView.as_view()), name='new'),
)
