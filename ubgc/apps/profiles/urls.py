from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required

from .views import DetailView, UpdateView,  SubmissionView

urlpatterns = patterns('',
    url(r'^(?P<pk>\d+)/$', DetailView.as_view(), name='detail'),
    url(r'^update/$', login_required(UpdateView.as_view()), name='update'),
    url(r'^submissions/$', login_required(SubmissionView.as_view()), name='submissions'),
)
