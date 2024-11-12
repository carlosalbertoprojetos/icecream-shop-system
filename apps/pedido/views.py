from django.shortcuts import redirect, get_object_or_404, render
from django.http import JsonResponse
from .models import Produto
from .utils import getCarrinhoDoCookies, salvarCarrinhoNoCookies, adicionarAoCarrinho, removerDoCarrinho


def adicionarAoCarrinho_view(request, product_id):
    product = get_object_or_404(Produto, id=product_id)
    quantity = int(request.POST.get('quantity', 1))

    cart = adicionarAoCarrinho(request, product_id, quantity)

    response = JsonResponse({'message': f'{product.name} foi adicionado ao carrinho.'})
    salvarCarrinhoNoCookies(response, cart)
    return response

def removerDoCarrinho(request, product_id):
    cart = removerDoCarrinho(request, product_id)

    response = JsonResponse({'message': 'Item removido do carrinho.'})
    salvarCarrinhoNoCookies(response, cart) #save_cart_to_cookies
    return response


def exibirCarrinho(request): #cart_view
    cart = getCarrinhoDoCookies(request) #get_cart_from_cookies
    products = Produto.objects.filter(id__in=cart.keys())
    
    # Calcula o total e organiza os itens no formato necessário
    cart_items = []
    total = 0
    for product in products:
        quantity = cart[str(product.id)]
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

    context = {
        'cart_items': cart_items,
        'total': total
    }
    return render(request, 'pedido/exibirCarrinho.html', context)
