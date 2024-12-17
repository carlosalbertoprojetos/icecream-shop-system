from django.urls import path
from . import views as v

app_name = "pedido"

urlpatterns = [
    path("checkout/", v.checkout, name="checkout"),
    path("criar/", v.criarPedido, name="criarPedido"),
    path("carrinho/", v.listarCarrinho, name="listarCarrinho"),
    path("finalizado/", v.pedidoFinalizado, name="pedidoFinalizado"),
    path("carrinho/adicionar/<int:produto_id>/", v.adicionarItem, name="adicionarItem"),
    path("carrinho/tirar/<int:produto_id>/", v.tirarItem, name="tirarItem"),
    path("carrinho/remover/<int:produto_id>/", v.removerItem, name="removerItem"),
    path("lista/", v.pedidosLista, name="pedidosLista"),
    # path("lista/cliente/<int:pk>/", v.pedidosClienteLista, name="pedidosClienteLista"),
]
