from django.views.generic import DetailView, UpdateView
from django.core.urlresolvers import reverse

from .models import Profile
from .forms import ProfileForm

class DetailView(DetailView):

    context_object_name = 'profile'
    model = Profile
    template_name = 'profiles/detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        profile = context['profile']
        return context


class UpdateView(UpdateView):

    model = Profile
    form_class = ProfileForm
    template_name = 'profiles/form.html'

    def get_object(self, *args, **kwargs):
        return self.request.user.profile

    def get_success_url(self, *args, **kwargs):
        return reverse("profiles:update")
