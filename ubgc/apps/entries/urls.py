from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required

from .views import CreateView

urlpatterns = patterns('',
    url(r'^new/$', login_required(CreateView.as_view()), name='new'),
)
