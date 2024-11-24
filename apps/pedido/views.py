import json
from decimal import Decimal
from django.http import JsonResponse
from django.shortcuts import render
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


@csrf_exempt
def adicionar_item(request, item_id):
    sacola = get_sacola(request)
    item = {"id": item_id, "quantidade": 1}

    for i in sacola:
        if i["id"] == item_id:
            i["quantidade"] += 1
            break
    else:
        sacola.append(item)

    total_itens = get_total_itens(sacola)
    response = JsonResponse({"status": "Item adicionado", "total_itens": total_itens})
    response.set_cookie("sacola", json.dumps(sacola))

    return response


def total_itens_sacola(request):
    sacola = get_sacola(request)
    sacola, total_acumulado = calcular_totais(sacola)  # Calcular os totais
    total_itens = get_total_itens(sacola)
    return JsonResponse(
        {
            "sacola": sacola,
            "total_itens": total_itens,
            "total_acumulado": total_acumulado,
        }
    )


@csrf_exempt
def remover_item(request, item_id):
    sacola = get_sacola(request)
    sacola = [item for item in sacola if item["id"] != item_id]

    response = JsonResponse({"status": "Item removido", "sacola": sacola})
    response.set_cookie("sacola", json.dumps(sacola))
    return response


def checkout(request):
    # Lógica de checkout, como exibir resumo da compra, etc.
    return render(request, "pedido/checkout.html")
