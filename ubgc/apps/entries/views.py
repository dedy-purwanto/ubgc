from django.views.generic import CreateView
from django.core.urlresolvers import reverse
from django.contrib import messages

from .models import Entry
from .forms import EntryForm

class CreateView(CreateView):

    model = Entry
    form_class = EntryForm
    template_name = 'entries/form.html'

    def get_object(self, *args, **kwargs):
        return self.request.user.profile

    def get_success_url(self, *args, **kwargs):
        messages.success(self.request, "Your entry has been submitted")
        return reverse("profiles:detail", args=[self.request.user.pk])
