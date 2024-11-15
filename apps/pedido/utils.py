import json


def getCarrinhoDoCookies(request):  # get_cart_from_cookies
    cart = request.COOKIES.get("cart")
    return json.loads(cart) if cart else {}


def salvarCarrinhoNoCookies(response, cart):  # save_cart_to_cookies
    response.set_cookie("cart", json.dumps(cart), max_age=2592000)  # Expira em 30 dias


def adicionarAoCarrinho(request, product_id, quantity):  # add_to_cart
    cart = getCarrinhoDoCookies(request)
    if product_id in cart:
        cart[product_id] += quantity
    else:
        cart[product_id] = quantity
    return cart


def removerDoCarrinho(request, product_id):  # remove_from_cart
    cart = salvarCarrinhoNoCookies(request)
    if product_id in cart:
        del cart[product_id]
    return cart
