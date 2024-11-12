from django.urls import path
from apps.cliente import views

urlpatterns = [
    path("cadastrar/", views.clienteCadastro, name="clienteCadastro"),
    path("busca_cep/", views.busca_cep, name="busca_cep"),
    # path("listar", views.listar, name="listar"),
    # path("editar", views.editar, name="menu"),
    # path("deletar", views.deletar, name="deletar"),
]
