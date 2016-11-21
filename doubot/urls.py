"""URLs do projeto doubot."""

from django.conf import settings, urls
from django.conf.urls import static

from . import views

urlpatterns = [
    urls.url(r'^$', views.index_view, name='index'),
]

urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [urls.url(r'^__debug__/', urls.include(debug_toolbar.urls))]
