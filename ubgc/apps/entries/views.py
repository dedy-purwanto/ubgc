from django.views.generic import CreateView
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect

from .models import Entry
from .forms import EntryForm

class CreateView(CreateView):

    model = Entry
    form_class = EntryForm
    template_name = 'entries/form.html'

    def form_valid(self, form):
        self.object = form.save(self.request.user)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self, *args, **kwargs):
        messages.success(self.request, "Your entry has been submitted")
        return reverse("profiles:detail", args=[self.request.user.pk])
