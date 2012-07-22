from django.views.generic import CreateView, UpdateView
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.shortcuts import get_object_or_404
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
        self.object = None
        form_class = self.get_form_class()

        form = form_class(request.POST or None, instance=self.get_object())

        screenshot_formset = self.ScreenshotFormSet(request.POST, 
                request.FILES, instance=self.get_object())

        if form.is_valid() and screenshot_formset.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(self.request.user)
        entry = self.get_object()
        screenshot_formset = self.ScreenshotFormSet(self.request.POST, 
                self.request.FILES, instance=entry)
        if screenshot_formset.is_valid():
            screenshot_formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(EntryCreateUpdateMixin, self).get_context_data(**kwargs)

        screenshot_formset = self.ScreenshotFormSet(self.request.POST or None, 
                self.request.FILES or None, instance=self.get_object())
        if screenshot_formset.is_valid():
            pass
        context['screenshot_formset'] = screenshot_formset

        return context


class CreateView(EntryCreateUpdateMixin, CreateView):

    def get_object(self, *args, **kwargs):
        if self.object is None:
            self.object = Entry()
        
        return self.object

    def get_success_url(self, *args, **kwargs):
        messages.success(self.request, "Your entry has been submitted")
        return reverse("profiles:detail", args=[self.request.user.pk])


class UpdateView(EntryCreateUpdateMixin, UpdateView):

    def get_object(self, *args, **kwargs):
        entry = get_object_or_404(Entry, pk=self.kwargs['pk'], user=self.request.user)
        return entry

    def get_success_url(self, *args, **kwargs):
        messages.success(self.request, "Your entry has been saved")
        return reverse("entries:edit", args=[self.get_object().pk])
