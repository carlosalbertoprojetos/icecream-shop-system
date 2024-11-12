from datetime import datetime
import json
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from datetime import datetime, timedelta

# import pywhatkit as kit

# from base.forms import PedidoUpdateForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from apps.cliente.models import Cliente
from apps.produto.models import Produto

def index(request):
    return render(request, "index.html")


# lista os produtos do menu
def menu(request):
    produtos = Produto.objects.filter(ativo=True)
    print(produtos)
    # embalagens = Embalagem.objects.filter(ativo=True)
    # tipo_sabor = TipoSabor.objects.filter(ativo=True)
    # coberturas = Cobertura.objects.filter(ativo=True)
    context = {
        "produtos": produtos,
        # "embalagens": embalagens,
        # "tipo_sabor": tipo_sabor,
        # "coberturas": coberturas,
    }
    return render(request, "menu.html", context)


# Adicionar itens no carrinho
@login_required(login_url="/admin/login/")
def adicionar_carrinho(request):
    # se request.user pertencer a algum grupo (nível de acesso)
    if request.user.groups.exists():
        cliente_id = request.GET.get("cliente_id")

        if cliente_id:
            cliente = Cliente.objects.get(id=cliente_id)
            print("Cliente selecionado:", cliente)
        else:
            cliente = request.user
            print("Cliente padrão:", cliente)
    else:
        cliente = request.user

    # Sua lógica para adicionar ao carrinho aqui
    return render(request, "carrinho.html", {"cliente": cliente})

    # if request.method == "POST":
    #     produto_id = request.POST.get("produto_id")
    #     produto = Produto.objects.get(id=produto_id)
    #     ultimo_pedido = Pedido.objects.filter(
    #         user=cliente, pago=False, entregue=False
    #     ).last()

    #     # Data de hoje
    #     # hoje = datetime.today().date()
    #     hoje = datetime.now().date()

    #     if ultimo_pedido != None:
    #         # verifica se o pedido foi realizado hoje
    #         ultimo_pedido_data = ultimo_pedido.data_pedido.date()

    #         if ultimo_pedido_data == hoje:
    #             # verifica há itens neste pedido e se este item já foi selecionado para este pedido
    #             if (
    #                 ItensCarrinho.objects.filter(pedido=ultimo_pedido.id).exists()
    #                 and not ItensCarrinho.objects.filter(
    #                     pedido=ultimo_pedido.id, produto=produto
    #                 ).exists()
    #             ):
    #                 ItensCarrinho.objects.create(pedido=ultimo_pedido, produto=produto)
    #                 # atualiza data/hora do pedido
    #                 ultimo_pedido.data_pedido = datetime.now()
    #                 ultimo_pedido.save()

    #         else:
    #             # cria um novo pedido e o item relacionado ao novo pedido
    #             novo_pedido = Pedido.objects.create(
    #                 user=cliente,
    #             )
    #             ItensCarrinho.objects.create(pedido=novo_pedido, produto=produto)
    #     else:
    #         # cria um novo pedido e o item relacionado ao novo pedido
    #         novo_pedido = Pedido.objects.create(
    #             user=cliente,
    #         )
    #         ItensCarrinho.objects.create(pedido=novo_pedido, produto=produto)

    return redirect("/menu/")

    # try:
    #     dados_str = request.POST.get("dados", None)
    #     dados = json.loads(dados_str)

    #     embalagem_id = dados.get("embalagem_id", None)
    #     quantidade_pote = int(dados.get("quantidade_pote", None))

    #     # Tente obter a sacola existente do usuário
    #     pedido = Pedido.objects.create(user=request.user, status=True).first()

    #     # Se não existir uma sacola, crie uma nova
    #     if not pedido:
    #         # Crie um novo pedido e associe a sacola criada
    #         pedido = Pedido.objects.create(
    #             user=request.user,
    #             status=True,
    #             itens_da_sacola=ItensCarrinho.objects.create(),
    #         )
    #     # monta_pote = MontaPote.objects.create(
    #     #     embalagem_id=embalagem_id, quantidade=quantidade_pote
    #     # )
    #     itens_carrinho = ItensCarrinho.objects.create(
    #         pedido=pedido, produto=produto, quantidade=quantidade, preco=preco
    #     )
    #     itens_carrinho.save()

    #     # for sabor in dados["sabores_selecionados"]:
    #     #     # Adicione os sabore ao pote durante a criação
    #     #     SelSabor.objects.create(
    #     #         pote=monta_pote,
    #     #         sabor_id=sabor["sabor_id"],
    #     #         quantidade_bolas=sabor["quantidade"],
    #     #     )

    #     # for cobertura in dados["cobertura_selecionadas"]:
    #     #     # Adicione as coberturas ao pote durante a criação
    #     #     SelCobertura.objects.create(
    #     #         pote=monta_pote,
    #     #         cobertura_id=cobertura["cobertura_id"],
    #     #         quantidade_cobertura=cobertura["quantidade"],
    #     #     )
    #     pedido.itens_da_sacola.potes.add(monta_pote)
    #     pedido.itens_da_sacola.preco_total()

    #     return JsonResponse(
    #         {
    #             "status": "success",
    #             "message": "Item adicionado na sacola com sucesso!!!",
    #         }
    #     )
    # except Exception as e:
    #     return JsonResponse({"status": "error", "message": str(e)})
    return JsonResponse({"status": "error", "message": "Requisição inválida."})


# @login_required(login_url="/admin/login/")
# def atualiza_quantidade_sacola(request):
#     if request.method == "POST":
#         pedido = Pedido.objects.filter(user=request.user, status=True).first()

#         pote_id = request.POST.get("poteId", None)
#         novaQuantidade = request.POST.get("novaQuantidade", None)

#         pote = get_object_or_404(MontaPote, id=pote_id)
#         pote.quantidade = int(novaQuantidade)
#         pote.save()

#         response = {
#             "status": "success",
#             "message": "Atualizado",
#             "novo_valor": f"R$ {pedido.itens_da_sacola.preco_total()}",
#         }
#         return JsonResponse(response)
#     else:
#         # Se a requisição não for do tipo POST, você pode retornar um erro ou outra resposta apropriada
#         return JsonResponse(
#             {"status": "error", "message": "Método não permitido"}, status=405
#         )


# @login_required(login_url="/admin/login/")
# def remove_item_sacola(request):
#     if request.method == "POST":
#         pedido = Pedido.objects.filter(user=request.user, status=True).first()

#         pote_id = request.POST.get("poteId", None)

#         # Verifique se o pote_id é fornecido
#         if not pote_id:
#             return JsonResponse(
#                 {"status": "error", "message": "ID do pote não fornecido"}, status=400
#             )

#         # Encontre o MontaPote específico
#         pote = get_object_or_404(MontaPote, id=pote_id)

#         # Exclua o pote
#         pote.delete()

#         response = {
#             "status": "success",
#             "message": "Item removido com sucesso",
#             "novo_valor": f"R$ {pedido.itens_da_sacola.preco_total()}",
#         }

#         return JsonResponse(response)
#     else:
#         # Se a requisição não for do tipo POST, você pode retornar um erro ou outra resposta apropriada
#         return JsonResponse(
#             {"status": "error", "message": "Método não permitido"}, status=405
#         )


# # finaliza o pedido
# @login_required(login_url="/admin/login/")
# def checkout_pedido(request):
#     pedido = Pedido.objects.filter(user=request.user, status=True).first()

#     if request.method == "POST":
#         form = PedidoUpdateForm(request.POST, instance=pedido)
#         if form.is_valid():
#             pedido = form.save(commit=False)
#             pedido.status = False
#             pedido.save()
#             messages.success(request, "Pedido atualizado com sucesso!")
#             return redirect("menu")
#     else:
#         form = PedidoUpdateForm(instance=pedido)

#     return render(request, "pedido/pedido.html", {"form": form, "pedido": pedido})


# # lista os pedidos do usuário
# @login_required(login_url="/admin/login/")
# def meus_pedidos(request):
#     if request.user.is_staff:
#         meus_pedidos = Pedido.objects.all()
#     else:
#         meus_pedidos = Pedido.objects.filter(user=request.user)
#     return render(request, "meus-pedidos.html", {"meus_pedidos": meus_pedidos})


# # lista pedidos geral
# @login_required(login_url="/admin/login/")
# def todos_pedidos(request):
#     if request.user.is_superuser:
#         todos_pedidos = Pedido.objects.all()
#     else:
#         # todos_pedidos = Pedido.objects.filter(user=request.user)
#         return redirect("menu")
#     return render(request, "gerencia-pedidos.html", {"todos_pedidos": todos_pedidos})


# # atualizar o pedido
# @login_required(login_url="/admin/login/")
# def atualizar_pedido(request):
#     dados_str = request.POST.get("dados", None)
#     dados = json.loads(dados_str)

#     pedido_id = dados.get("id", None)
#     status = dados.get("status", None)
#     pago = dados.get("pago", None)
#     entrega = dados.get("entrega", None)

#     print(pedido_id, status, pago, entrega)
#     try:
#         pedido = Pedido.objects.get(pk=pedido_id)
#         pedido.status = status
#         pedido.pago = pago
#         pedido.entrega = entrega
#         pedido.save()
#         return JsonResponse({"success": True})
#     except Pedido.DoesNotExist:
#         return JsonResponse({"success": False, "error": "Pedido não encontrado"})
#     except Exception as e:
#         return JsonResponse({"success": False, "error": str(e)})


# # enviar mensagem whatsapp
# def enviar_whatsapp_pedido(request):
#     pedido_id = request.POST.get("pedido_id", None)

#     try:
#         pedido = Pedido.objects.get(pk=pedido_id)
#         # Número de telefone com código de país (por exemplo, +55 para BRA)
#         numero = "+5531986766866"

#         mensagem = f"""
# Data do Pedido: {pedido.data_pedido.strftime('%d/%m/%Y %H:%M:%S')}
# Status do Pedido: {'✅' if pedido.status else '❌'}
# Status do Pagamento: {'✅' if pedido.pago else '❌'}
# Status da Entrega: {'✅' if pedido.entrega else '❌'}

# Detalhes do Pedido:
# {format_message(pedido)}

# Tempo estimado de entrega: 60min\n
#         """

#         # Envie a mensagem
#         kit.sendwhatmsg_instantly(numero, mensagem)
#         return JsonResponse({"success": mensagem})
#     except Pedido.DoesNotExist:
#         return JsonResponse({"success": False, "error": "Pedido não encontrado"})
#     except Exception as e:
#         return JsonResponse({"success": False, "error": str(e)})


# def format_message(pedido):
#     detalhes = []
#     for pote in pedido.itens_da_sacola.potes.all():
#         detalhes.append(f"\nPote:  {pote.quantidade} x {pote.embalagem.tipo}\n")
#         sabores_str = "".join(
#             [
#                 f"\n- {sel_sabor.quantidade_bolas} x {sel_sabor.sabor.nome}"
#                 for sel_sabor in pote.pote.all()
#             ]
#         )
#         detalhes.append(f"Sabor(es):{sabores_str}\n")
#         descricao_coberturas = pote.obter_descricao_coberturas()
#         if descricao_coberturas:
#             detalhes.append("\nAdicionais:\n")
#             detalhes.extend(f"- {desc}\n" for desc in descricao_coberturas.split(";"))
#     detalhes.append(f"\nValor Total: R$ {pedido.itens_da_sacola.preco_total()}")
#     return "".join(detalhes)
