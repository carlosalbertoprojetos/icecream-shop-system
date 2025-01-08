import requests
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum


from apps.produto.models import Produto
from apps.pedido.models import FormaPagamento, ItensCarrinho, Pedido


def checkout(request):
    lista_forma_pagamento = FormaPagamento.objects.all()
    # Lógica de checkout, como exibir resumo da compra, etc.
    context = {"lista_forma_pagamento": lista_forma_pagamento}
    return render(request, "pedido/checkout.html", context)


def calcular_quantidade_carrinho(carrinho):
    return sum(item["quantidade"] for item in carrinho.values())


def adicionarItem(request, produto_id):
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
            "id_prod": produto.id,
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

    # Retorna a resposta JSON com o carrinho atualizado e a quantidade total
    return JsonResponse(
        {
            "quantidade_total": quantidade_total,
            "carrinho": carrinho,
        }
    )


def tirarItem(request, produto_id):
    # Obtém o carrinho da sessão, ou inicializa como vazio
    carrinho = request.session.get("carrinho", {})

    # Adiciona ou incrementa a quantidade do produto no carrinho
    if str(produto_id) in carrinho:
        carrinho[str(produto_id)]["quantidade"] -= 1

    # Atualiza o total de cada item no carrinho
    for key, item in carrinho.items():
        item["total"] = item["preco"] * item["quantidade"]

    # Calcula a quantidade total de itens no carrinho
    quantidade_total = calcular_quantidade_carrinho(carrinho)

    # Salva o carrinho na sessão
    request.session["carrinho"] = carrinho

    # Retorna a resposta JSON com o carrinho atualizado e a quantidade total
    return JsonResponse(
        {
            "quantidade_total": quantidade_total,
            "carrinho": carrinho,
        }
    )


def removerItem(request, produto_id):
    # Obtém o carrinho da sessão
    carrinho = request.session.get("carrinho", {})

    # Remove o produto do carrinho, se existir
    if str(produto_id) in carrinho:
        del carrinho[str(produto_id)]

    calcular_quantidade_carrinho(carrinho)

    # Salva o carrinho atualizado na sessão
    request.session["carrinho"] = carrinho

    return redirect("pedido:listarCarrinho")


def listarCarrinho(request):
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


@login_required(login_url="/admin/login/?next=/admin/")
def criarPedido(request):
    if request.method == "POST":
        bd_forma_pagamento = request.POST.get("forma_pagamento")
        forma_pagamento = FormaPagamento.objects.get(id=bd_forma_pagamento)

        # Obtém o carrinho da sessão, ou inicializa como vazio
        carrinho = request.session.get("carrinho", {})

        total_geral = 0
        # Calcula o total geral
        for key, item in carrinho.items():
            preco = item["preco"]
            quantidade = item["quantidade"]
            total_geral += preco * quantidade

        pedido = Pedido.objects.create(
            usuario=request.user,
            forma_pagamento=forma_pagamento,
            total=total_geral,
            atendente=request.user,
        )

        # Iterando pelos itens e imprimindo os preços
        for key, item in carrinho.items():
            ItensCarrinho.objects.create(
                pedido=pedido,
                produto=Produto.objects.get(id=key),
                quantidade=item["quantidade"],
                preco=item["preco"],
            )

    # Limpa a sessão após criar o pedido
    # request.session.flush()

    return redirect("pedido:pedidoFinalizado", pedido.id)


# View para buscar endereço a partir do CEP
def buscaCep(request):
    cep = request.GET.get("cep")
    response = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
    data = response.json()

    return JsonResponse(data)


def pedidoFinalizado(request, pedido_id):
    pedido = Pedido.objects.get(id=pedido_id)
    bd_itens = ItensCarrinho.objects.filter(pedido__id=pedido_id)

    # Calcula o total de cada item (preço * quantidade)
    itens = [
        {
            "id": item.id,
            "produto": item.produto,
            "preco": item.produto.preco,
            "quantidade": item.quantidade,
            "total": item.produto.preco * item.quantidade,
        }
        for item in bd_itens
    ]

    template_name = "pedido/pedidoFinalizado.html"
    context = {"pedido": pedido, "itens": itens}
    return render(request, template_name, context)


def pedidosLista(request):
    pedidos = Pedido.objects.filter(usuario=request.user)
    itens = ItensCarrinho.objects.filter(pedido__usuario=request.user)

    # Contagem de pedidos e soma do valor dos pedidos
    num_pedidos = pedidos.count()  # Quantidade de pedidos
    total_valor = pedidos.aggregate(Sum("total"))[
        "total__sum"
    ]  # Soma do valor dos pedidos

    # Passando as variáveis para o contexto
    context = {
        "pedidos": pedidos,
        "itens": itens,
        "num_pedidos": num_pedidos,
        "total_valor": total_valor,
    }
    template_name = "pedido/pedidosList.html"
    return render(request, template_name, context)
