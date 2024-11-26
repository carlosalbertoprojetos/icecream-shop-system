import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from apps.produto.models import Produto


def get_sacola(request):
    # Dados simulando o retorno de request.session.items()
    session_data = request.session.items()
    sacola = dict(session_data).get("sacola", None)
    return sacola


def get_total_itens(sacola):
    return sum(float(item["quantidade"]) for item in sacola)


def calcular_totais(sacola):
    """Calcula os totais para os itens da sacola."""
    total_acumulado = 0

    for item in sacola:
        produto = Produto.objects.filter(id=item["id"]).first()
        # Verificando se o item é um dicionário
        if isinstance(item, dict):
            # Certifique-se de que 'preco' seja um número (string ou número)
            item["preco"] = float(produto.preco)
            item["total_preco"] = item["preco"] * item["quantidade"]
            total_acumulado += item["total_preco"]
        else:
            # print(f"Item inválido: {item}")
            continue  # Pule este item se não for um dicionário

    return sacola, total_acumulado


# @csrf_exempt
# def adicionar_item(request, item_id):
#     sacola = get_sacola(request)
#     item = {"id": item_id, "quantidade": 1}

#     for i in sacola:
#         if i["id"] == item_id:
#             i["quantidade"] += 1
#             break
#     else:
#         sacola.append(item)

#     total_itens = get_total_itens(sacola)
#     response = JsonResponse({"status": "Item adicionado", "total_itens": total_itens})
#     response.set_cookie("sacola", json.dumps(sacola))

#     return response


def total_itens_sacola(request):
    sacola = get_sacola(request)
    sacola, total_acumulado = calcular_totais(sacola)  # Calcular os totais
    total_itens = get_total_itens(sacola)

    # Formatar os dados para serem renderizados no template
    # sacola_formatada = [
    #     {
    #         "id": item.get("id"),
    #         "nome": item.get("nome"),
    #         "quantidade": item.get("quantidade"),
    #         "preco": item.get("preco"),
    #         "total": item.get("total"),
    #     }
    #     for item in sacola
    # ]

    return JsonResponse(
        {
            # "sacola_formatada": sacola_formatada,
            "sacola": sacola,
            "total_itens": total_itens,
            "total_acumulado": total_acumulado,
        }
    )


# @csrf_exempt
# def remover_item(request, item_id):
#     sacola = get_sacola(request)
#     sacola = [item for item in sacola if item["id"] != item_id]

#     response = JsonResponse({"status": "Item removido", "sacola": sacola})
#     response.set_cookie("sacola", json.dumps(sacola))
#     return response


def checkout(request):
    # Lógica de checkout, como exibir resumo da compra, etc.
    return render(request, "pedido/checkout.html")


from .utils import adicionar_ao_carrinho, remover_do_carrinho


# def adicionar_item(request, produto_id):
#     adicionar_ao_carrinho(request, produto_id)
#     return redirect("produto:listar_produtos")


from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Produto


def adicionar_item(request, produto_id):
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

    # Calcula a quantidade total de itens no carrinho
    quantidade_total = sum(item["quantidade"] for item in carrinho.values())

    # Salva o carrinho na sessão
    request.session["carrinho"] = carrinho

    # Retorna a resposta JSON com o carrinho atualizado e a quantidade total
    return JsonResponse(
        {
            "quantidade_total": quantidade_total,
            "carrinho": carrinho,
        }
    )


def remover_item(request, produto_id):
    remover_do_carrinho(request, produto_id)
    return redirect("pedido:listar_carrinho")


def listar_carrinho(request):
    carrinho = request.session.get("carrinho", {})
    # Calcula o total do pedido somando os valores totais dos itens
    total_pedido = sum(item["total"] for item in carrinho.values())

    # Retorna o carrinho e o total do pedido como contexto para o template
    context = {
        "carrinho": carrinho,
        "total_pedido": total_pedido,
    }
    return render(request, "pedido/carrinho.html", context)
