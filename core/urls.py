from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView


urlpatterns = [
    path(
        "",
        (TemplateView.as_view(template_name="index.html")),
        name="index",
    ),
    path("admin/", admin.site.urls),
    path("cliente/", include("apps.cliente.urls")),
    path("pedido/", include("apps.pedido.urls")),
    path("produto/", include("apps.produto.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
