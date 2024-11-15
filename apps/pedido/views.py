import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from apps.produto.models import Produto


def get_sacola(request):
    sacola = json.loads(request.COOKIES.get("sacola", "[]"))
    return sacola


def get_total_itens(sacola):
    return sum(item["quantidade"] for item in sacola)


def calcular_totais(sacola):
    total_geral = 0
    for item in sacola:
        produto = Produto.objects.get(id=item["id"])  # Obter produto pelo id

        # Verifique os campos corretos para obter uma string
        tipo_mercadoria = (
            produto.base.tipo.nome
        )  # Supondo que 'nome' seja o atributo correto
        sabor = (
            produto.sabor.nome
        )  # Supondo que 'nome' seja o atributo que você quer do objeto 'Sabor'

        # Agora você pode concatenar as strings
        item["nome"] = f"{tipo_mercadoria} {sabor}"
        item["preco"] = produto.preco
        item["total"] = item["quantidade"] * produto.preco  # Total por item
        total_geral += item["total"]  # Soma para o total geral
    return sacola, total_geral


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
    total_itens = get_total_itens(sacola)
    return JsonResponse({"total_itens": total_itens})


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
