from django.views.generic import CreateView, UpdateView
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.forms.models import inlineformset_factory

from .models import Entry, Screenshot
from .forms import EntryForm, ScreenshotForm

class EntryCreateUpdateMixin(object):

    model = Entry
    form_class = EntryForm
    template_name = 'entries/form.html'
    ScreenshotFormSet = inlineformset_factory(Entry, Screenshot,
            can_delete=True, extra=3, form=ScreenshotForm)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()

        pk = self.kwargs.get('pk', None)

        if pk is not None:
            form = form_class(self.request.POST or None, 
                    instance=self.get_object())
        else:
            form = form_class(self.request.POST or None)

        screenshot_formset = self.ScreenshotFormSet(self.request.POST or None, 
                self.request.FILES or None)
        if form.is_valid() and screenshot_formset.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(self.request.user)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(EntryCreateUpdateMixin, self).get_context_data(**kwargs)

        screenshot_formset = self.ScreenshotFormSet(self.request.POST or None, self.request.FILES or None)
        context['screenshot_formset'] = screenshot_formset
        
        return context


class CreateView(EntryCreateUpdateMixin, CreateView):

    def get_success_url(self, *args, **kwargs):
        messages.success(self.request, "Your entry has been submitted")
        return reverse("profiles:detail", args=[self.request.user.pk])


class UpdateView(EntryCreateUpdateMixin, UpdateView):

    def get_object(self, *args, **kwargs):
        pk = self.kwargs['pk']
        return Entry.objects.get(pk=pk, user=self.request.user)

    def get_success_url(self, *args, **kwargs):
        messages.success(self.request, "Your entry has been saved")
        return reverse("entries:edit", args=[self.get_object().pk])
