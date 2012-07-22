from django.views.generic import TemplateView

from entries.models import Entry

class HomeView(TemplateView):

    template_name = "home/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        entries = Entry.objects.filter(disabled=False)
        top_entries = entries.order_by('-num_votes')
        recent_entries = entries.order_by('-date_modified')

        context['top_entries'] = top_entries
        context['recent_entries'] = recent_entries

        return context
