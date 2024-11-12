from django.urls import path
from . import views as v

urlpatterns = [
    path('adicionar/<int:product_id>/', v.adicionarAoCarrinho_view, name='adicionarAoCarrinho_view'),
    path('remover/<int:product_id>/', v.removerDoCarrinho, name='removerDoCarrinho'),
    path('carrinho/', v.exibirCarrinho, name='exibirCarrinho')
]
