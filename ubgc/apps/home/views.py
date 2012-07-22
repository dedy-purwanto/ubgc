from django.views.generic import TemplateView

class HomeView(TemplateView):

    template_name = "home/home.html"

    def render_to_response(self, context, **response_kwargs):

        return super(HomeView, self).render_to_response(context, **response_kwargs)

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        return context
