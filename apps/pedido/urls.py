from django.urls import path
from . import views as v

app_name = "pedido"

urlpatterns = [
    path("adicionar-item/<int:item_id>/", v.adicionar_item, name="adicionar_item"),
    path("remover-item/<int:item_id>/", v.remover_item, name="remover_item"),
    path("sacola-itens/", v.total_itens_sacola, name="total_itens_sacola"),
    path("checkout/", v.checkout, name="checkout_pedido"),
]
