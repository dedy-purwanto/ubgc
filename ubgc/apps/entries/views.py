from django.views.generic import CreateView, UpdateView, DetailView, \
        TemplateView, DeleteView
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.forms.models import inlineformset_factory

from .models import Entry, Screenshot, Vote
from .forms import EntryForm, ScreenshotForm, VoteForm

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


class EntryCreateView(EntryCreateUpdateMixin, CreateView):

    def get_object(self, *args, **kwargs):
        if self.object is None:
            self.object = Entry()
        
        return self.object

    def get_success_url(self, *args, **kwargs):
        messages.success(self.request, "Your entry has been submitted")
        return reverse("profiles:detail", args=[self.request.user.pk])


class EntryUpdateView(EntryCreateUpdateMixin, UpdateView):

    def get_object(self, *args, **kwargs):
        entry = get_object_or_404(Entry, pk=self.kwargs['pk'], user=self.request.user)
        return entry

    def get_success_url(self, *args, **kwargs):
        messages.success(self.request, "Your entry has been saved")
        return reverse("entries:edit", args=[self.get_object().pk])


class EntryDeleteView(DeleteView):

    template_name = 'entries/delete.html'

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Entry, pk=self.kwargs['pk'], user=self.request.user)

    def get_success_url(self, *args, **kwargs):
        messages.success(self.request, "Your entry has been removed")
        return reverse("profiles:submissions")


class DetailView(DetailView):

    context_object_name = 'entry'
    model = Entry
    template_name = 'entries/detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        entry = context['entry']

        can_vote = False
        if self.request.user.is_authenticated():
            try:
                Vote.objects.get(entry=entry, user=self.request.user)
            except Vote.DoesNotExist:
                can_vote = True

        context['can_vote'] = can_vote

        return context


class VoteCreateView(CreateView):

    model = Vote
    form_class = VoteForm
    template_name = 'entries/votes_form.html'

    def form_valid(self, form):
        entry = Entry.objects.get(pk=self.kwargs['pk'])
        self.object = form.save(self.request.user, entry)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self, *args, **kwargs):
        entry = self.object.entry
        messages.success(self.request, "Your vote has been saved")
        return reverse("entries:play", args=[entry.pk, entry.slug])


class VoteListView(TemplateView):

    template_name = 'entries/votes_list.html'

    def get_context_data(self, **kwargs):
        context = super(VoteListView, self).get_context_data(**kwargs)

        given = Vote.objects.filter(user=self.request.user)
        received = Vote.objects.filter(entry__user=self.request.user)

        context['votes_given'] = given
        context['votes_received'] = received

        return context


class VoteDeleteView(DeleteView):

    template_name = 'entries/votes_delete.html'

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Vote, pk=self.kwargs['pk'], user=self.request.user)

    def get_success_url(self, *args, **kwargs):
        messages.success(self.request, "Your vote has been removed")
        return reverse("entries:votes")
