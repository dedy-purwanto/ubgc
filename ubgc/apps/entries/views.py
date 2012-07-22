from django.views.generic import CreateView
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.forms.models import inlineformset_factory

from .models import Entry, Screenshot
from .forms import EntryForm, ScreenshotForm

class CreateView(CreateView):

    model = Entry
    form_class = EntryForm
    template_name = 'entries/form.html'
    ScreenshotFormSet = inlineformset_factory(Entry, Screenshot,
            can_delete=True, extra=3, form=ScreenshotForm)

    def form_valid(self, form):
        self.object = form.save(self.request.user)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self, *args, **kwargs):
        messages.success(self.request, "Your entry has been submitted")
        return reverse("profiles:detail", args=[self.request.user.pk])

    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)

        screenshot_formset = self.ScreenshotFormSet(self.request.POST or None)
        context['screenshot_formset'] = screenshot_formset

        
        return context


class UpdateView(CreateView):

    def get_success_url(self, *args, **kwargs):
        messages.success(self.request, "Your entry has been saved")
        return reverse("profiles:detail", args=[self.request.user.pk])
