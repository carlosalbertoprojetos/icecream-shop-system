# import json


# def getCarrinhoDoCookies(request):  # get_cart_from_cookies
#     cart = request.COOKIES.get("cart")
#     return json.loads(cart) if cart else {}


# def salvarCarrinhoNoCookies(response, cart):  # save_cart_to_cookies
#     response.set_cookie("cart", json.dumps(cart), max_age=2592000)  # Expira em 30 dias


# def adicionarAoCarrinho(request, product_id, quantity):  # add_to_cart
#     cart = getCarrinhoDoCookies(request)
#     if product_id in cart:
#         cart[product_id] += quantity
#     else:
#         cart[product_id] = quantity
#     return cart


# def removerDoCarrinho(request, product_id):  # remove_from_cart
#     cart = salvarCarrinhoNoCookies(request)
#     if product_id in cart:
#         del cart[product_id]
#     return cart


from django.shortcuts import get_object_or_404
from apps.produto.models import Produto


def calcular_quantidade_carrinho(carrinho):
    return sum(item["quantidade"] for item in carrinho.values())


def adicionar_ao_carrinho(request, produto_id):
    # Obtém o carrinho da sessão, ou inicializa como vazio
    carrinho = request.session.get("carrinho", {})

    # Verifica se o produto existe
    produto = get_object_or_404(Produto, id=produto_id)

    # Adiciona ou incrementa a quantidade do produto no carrinho
    if str(produto_id) in carrinho:
        carrinho[str(produto_id)]["quantidade"] += 1
    else:
        carrinho[str(produto_id)] = {
            "nome": str(produto.base),
            "preco": float(produto.preco),
            "quantidade": 1,
        }

    # Atualiza o total de cada item no carrinho
    for key, item in carrinho.items():
        item["total"] = item["preco"] * item["quantidade"]

    calcular_quantidade_carrinho(carrinho)

    # Salva o carrinho na sessão
    request.session["carrinho"] = carrinho


def remover_do_carrinho(request, produto_id):
    # Obtém o carrinho da sessão
    carrinho = request.session.get("carrinho", {})

    # Remove o produto do carrinho, se existir
    if str(produto_id) in carrinho:
        del carrinho[str(produto_id)]

    calcular_quantidade_carrinho(carrinho)

    # Salva o carrinho atualizado na sessão
    request.session["carrinho"] = carrinho


def listar_carrinho(request):
    carrinho = request.session.get("carrinho", {})
    return {
        "carrinho": carrinho,
    }
