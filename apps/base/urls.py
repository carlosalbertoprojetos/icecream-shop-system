from django.urls import path
from apps.base import views as v

urlpatterns = [
    path("", v.index, name="index"),
    path("menu/", v.menu, name="menu"),
    path("carrinho/", v.adicionar_carrinho, name="adicionar_carrinho"),
    # path(
    #     "atualiza_quantidade_sacola/",
    #     views.atualiza_quantidade_sacola,
    #     name="atualiza_quantidade_sacola",
    # ),
    # path("remove_item_sacola/", views.remove_item_sacola, name="remove_item_sacola"),
    # path("checkout-pedido/", views.checkout_pedido, name="checkout_pedido"),
    # path("meus-pedidos/", views.meus_pedidos, name="meus_pedidos"),
    # path("gerencia-pedidos/", views.todos_pedidos, name="todos_pedidos"),
    # path("atualizar-pedido/", views.atualizar_pedido, name="atualizar_pedido"),
    # path(
    #     "enviar-pedido-whatsapp/",
    #     views.enviar_whatsapp_pedido,
    #     name="enviar_whatsapp_pedido",
    # ),
]
