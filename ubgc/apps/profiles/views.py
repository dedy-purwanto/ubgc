from django.views.generic import DetailView, UpdateView, TemplateView
from django.core.urlresolvers import reverse
from django.contrib import messages

from entries.models import Vote

from .models import Profile
from .forms import ProfileForm

class SubmissionView(TemplateView):

    template_name = 'profiles/submissions.html'


class VotesView(TemplateView):

    template_name = 'profiles/votes.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)

        given = Vote.objects.filter(user=self.request.user)
        received = Vote.objects.filter(entry__user=self.request.user)

        context['votes_given'] = given
        context['votes_received'] = received

        return context


class DetailView(DetailView):

    context_object_name = 'profile'
    model = Profile
    template_name = 'profiles/detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        profile = context['profile']
        context['votes_given'] = Vote.objects.filter(user=profile.user)
        context['votes_received'] = Vote.objects.filter(entry__user=profile.user)
        return context


class UpdateView(UpdateView):

    model = Profile
    form_class = ProfileForm
    template_name = 'profiles/form.html'

    def get_object(self, *args, **kwargs):
        return self.request.user.profile

    def get_success_url(self, *args, **kwargs):
        messages.success(self.request, "Your profile has been saved")
        return reverse("profiles:update")
