"""Views genéricas do projeto doubot."""

from django.views import generic


class IndexView(generic.TemplateView):
    """Index."""

    template_name = 'index.html'


index_view = IndexView.as_view()
