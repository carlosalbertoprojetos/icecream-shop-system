# from project import models


from apps.pedido.models import Pedido


def context_social(request):
    return {"social": "Exibir este contexto em qualquer lugar!"}


def context_sacola(request):
    return


def carrinho_context(request):
    carrinho = request.session.get("carrinho", {})
    quantidade_total = sum(item["quantidade"] for item in carrinho.values())
    return {"quantidade_carrinho": quantidade_total}


#     if request.user.is_authenticated:
#         # Recupere o pedido do usuário com status True (Ativo)
#         pedidos = Pedido.objects.filter(user=request.user)

#         # Inicialize a variável total_itens
#         total_itens = 0

#         # Itere sobre para contar o número total de itens em todas as sacolas
#         for pedido in pedidos:
#             total_itens += pedido.itens_da_sacola.potes.count()

#         # Recupere o ID da primeira sacola se existir
#         sacola = pedidos.first().itens_da_sacola if pedidos else None

#         # Retorne os resultados
#         return {"sacola_itens": sacola, "total_itens": total_itens}
#     else:
#         return {}
