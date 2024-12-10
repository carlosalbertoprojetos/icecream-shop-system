from django.urls import path
from . import views as v

app_name = "pedido"

urlpatterns = [
    path("checkout/", v.checkout, name="checkout_pedido"),
    path("carrinho/", v.listar_carrinho, name="listar_carrinho"),
    path("carrinho/adicionar/<int:produto_id>/", v.adicionarItem, name="adicionarItem"),
    path("carrinho/tirar/<int:produto_id>/", v.tirarItem, name="tirarItem"),
    path("carrinho/remover/<int:produto_id>/", v.removerItem, name="removerItem"),
]
