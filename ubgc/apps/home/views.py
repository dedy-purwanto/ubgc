from django.views.generic import TemplateView
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from entries.models import Entry

class HomeView(TemplateView):

    template_name = "home/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        entries = Entry.objects.filter(disabled=False)
        top_entries = entries.order_by('-num_votes')
        recent_entries = entries.order_by('-date_modified')

        context['top_entries'] = top_entries[:15]
        context['recent_entries'] = recent_entries

        return context


class LogOutView(TemplateView):

    def render_to_response(self, context, **response_kwargs):
        messages.success(self.request, "Your have been succesfully logged out")
        logout(self.request)

        return redirect(reverse("home"))

