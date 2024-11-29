from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404


from apps.produto.models import Produto


def checkout(request):
    # Lógica de checkout, como exibir resumo da compra, etc.
    return render(request, "pedido/checkout.html")


def calcular_quantidade_carrinho(carrinho):
    return sum(item["quantidade"] for item in carrinho.values())


def adicionar_item(request, produto_id):
    # Obtém o carrinho da sessão, ou inicializa como vazio
    carrinho = request.session.get("carrinho", {})

    # Verifica se o produto existe
    produto = get_object_or_404(Produto, id=produto_id)

    # Adiciona ou incrementa a quantidade do produto no carrinho
    if str(produto_id) in carrinho:
        carrinho[str(produto_id)]["quantidade"] += 1
    else:
        # quant = carrinho[str(produto_id)]["quantidade"]
        quant = 1
        carrinho[str(produto_id)] = {
            "nome": str(produto.base),
            "preco": float(produto.preco),
            "quantidade": quant,
            "total": quant * produto.preco,
        }

    # Atualiza o total de cada item no carrinho
    for key, item in carrinho.items():
        item["total"] = item["preco"] * item["quantidade"]

    # Calcula a quantidade total de itens no carrinho
    quantidade_total = calcular_quantidade_carrinho(carrinho)

    # calcular_quantidade_carrinho(carrinho)

    # Salva o carrinho na sessão
    request.session["carrinho"] = carrinho

    listar_carrinho(request)

    # Retorna a resposta JSON com o carrinho atualizado e a quantidade total
    return JsonResponse(
        {
            "quantidade_total": quantidade_total,
            "carrinho": carrinho,
        }
    )


def remover_item(request, produto_id):
    # Obtém o carrinho da sessão
    carrinho = request.session.get("carrinho", {})

    # Remove o produto do carrinho, se existir
    if str(produto_id) in carrinho:
        del carrinho[str(produto_id)]

    calcular_quantidade_carrinho(carrinho)

    # Salva o carrinho atualizado na sessão
    request.session["carrinho"] = carrinho

    return redirect("pedido:listar_carrinho")


# def listar_carrinho(request):
#     carrinho = request.session.get("carrinho", {})
#     # Calcula o total do pedido somando os valores totais dos itens
#     total_pedido = sum(item["total"] for item in carrinho.values())


#     # Retorna o carrinho e o total do pedido como contexto para o template
#     context = {
#         "carrinho": carrinho,
#         "total_pedido": total_pedido,
#     }
#     return render(request, "pedido/carrinho.html", context)


def listar_carrinho(request):
    carrinho = request.session.get("carrinho", {})

    # Calcula o total do pedido somando os valores totais dos itens
    total_pedido = sum(item["total"] for item in carrinho.values())

    # Retorna a resposta JSON com o carrinho atualizado e a quantidade total
    return JsonResponse(
        {
            "carrinho": carrinho,
            "total_pedido": total_pedido,
        }
    )
