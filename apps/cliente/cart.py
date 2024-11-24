# cart.py
from decimal import Decimal
from django.conf import settings
from .models import Produto


class Carrinho:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, produto, quantidade=1, override_quantidade=False):
        produto_id = str(produto.id)
        if produto_id not in self.cart:
            self.cart[produto_id] = {"quantidade": 0, "preco": str(produto.preco)}

        if override_quantidade:
            self.cart[produto_id]["quantidade"] = quantidade
        else:
            self.cart[produto_id]["quantidade"] += quantidade

        self.save()

    def remove(self, produto):
        produto_id = str(produto.id)
        if produto_id in self.cart:
            del self.cart[produto_id]
            self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        produto_ids = self.cart.keys()
        produtos = Produto.objects.filter(id__in=produto_ids)
        for produto in produtos:
            self.cart[str(produto.id)]["produto"] = produto

        for item in self.cart.values():
            item["preco"] = Decimal(item["preco"])
            item["total_preco"] = item["preco"] * item["quantidade"]
            yield item

    def __len__(self):
        return sum(item["quantidade"] for item in self.cart.values())

    def get_total_preco(self):
        return sum(
            Decimal(item["preco"]) * item["quantidade"] for item in self.cart.values()
        )

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
