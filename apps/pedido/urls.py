from django.urls import path
from . import views as v

app_name = "pedido"

urlpatterns = [
    path("checkout/", v.checkout, name="checkout_pedido"),
    path("carrinho/", v.listar_carrinho, name="listar_carrinho"),
    path(
        "carrinho/adicionar/<int:produto_id>/", v.adicionar_item, name="adicionar_item"
    ),
    path("carrinho/remover/<int:produto_id>/", v.remover_item, name="remover_item"),
]
