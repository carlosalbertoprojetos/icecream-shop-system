from django.urls import path
from apps.produto import views



urlpatterns = [
    path("cadastrar/", views.produtoCreate, name="produtoCreate"),
    # path("listar", views.listar, name="listar"),
    # path("editar", views.editar, name="menu"),
    # path("deletar", views.deletar, name="deletar"),
]
