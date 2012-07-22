from django.views.generic import DetailView

from .models import Profile

class DetailView(DetailView):

    context_object_name = 'profile'
    model = Profile
    template_name = 'profiles/detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        profile = context['profile']
        return context
