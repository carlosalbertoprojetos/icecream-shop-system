from django.urls import path
from apps.produto import views


app_name = "produto"


urlpatterns = [
    # path("cadastrar/", views.produtoCreate, name="produtoCreate"),
    path("listar", views.listar_produtos, name="listar_produtos"),
    # path("editar", views.editar, name="menu"),
    # path("deletar", views.deletar, name="deletar"),
]
