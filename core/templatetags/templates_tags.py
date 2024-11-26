from django import template


from apps.produto.models import Produto


register = template.Library()


@register.inclusion_tag("includes/menu.html", takes_context=True)
def show_menu(context):
    itens = Produto.objects.filter(ativo=True)
    embalagens = (
        Produto.objects.filter(ativo=True)
        .values("base__embalagem__id", "base__embalagem__nome")
        .distinct()
    )

    context.update({"embalagens": embalagens, "itens": itens})
    return context


# @register.inclusion_tag("includes/wallet.html", takes_context=True)
# def show_wallet(context):
#     request = context["request"]
#     sacola = get_sacola(request)
#     sacola, total_geral = calcular_totais(sacola)
#     total_itens = get_total_itens(sacola)

#     # Calcula os itens detalhados e o total acumulado
#     itens_detalhados = []
#     total_acumulado = 0

#     for item in sacola:
#         produto = Produto.objects.get(id=item["id"])
#         quantidade = item["quantidade"]
#         total_item = quantidade * produto.preco
#         total_acumulado += total_item

#         itens_detalhados.append(
#             {
#                 "nome": produto.sabor,
#                 "quantidade": quantidade,
#                 "preco_unitario": produto.preco,
#                 "total": total_item,
#             }
#         )

#     context = {"sacola": sacola, "total_itens": total_itens, "total_geral": total_geral}
#     return context


# @register.inclusion_tag("includes/abordagem.html")
# def show_abordagem():
#     abordagem = Abordagem.objects.filter(atual=True)
#     indice = IndicesAbordagem.objects.all()
#     indice_abordagem = TextosIndiceAbordagem.objects.all()
#     context = {
#         "abordagem": abordagem,
#         "indice": indice,
#         "indice_abordagem": indice_abordagem,
#     }
#     return context


# @register.inclusion_tag("includes/experiencia.html")
# def show_experiencia():
#     experiencia = Experiencia.objects.filter(atual=True)
#     data_desejada = datetime.now()
#     # filtra os objetos publicados com data de publicação maior ou igual à hoje
#     card = Card.objects.filter(
#         publicado=True,
#         data_publicacao__isnull=False,
#         data_publicacao__lte=data_desejada,
#     )

#     # Filtra o ID mais recente de cada grupo onde publicado é True
#     latest_ids = (
#         Card.objects.filter(
#             publicado=True,
#             data_publicacao__isnull=False,
#             data_publicacao__lte=data_desejada,
#         )
#         .values("grupo")
#         .annotate(latest_id=Max("id"))
#         .values_list("latest_id", flat=True)
#     )

#     # Filtra os grupos associados aos IDs mais recentes obtidos acima
#     grupos = Card.objects.filter(id__in=latest_ids).values("grupo__nome").distinct()

#     context = {
#         "experiencia": experiencia,
#         "grupos": grupos,
#         "card": card,
#     }
#     return context


# @register.inclusion_tag("includes/cardExperiencia.html")
# def show_card_experiencia(card_id):
#     data_desejada = datetime.now()

#     # Use get_object_or_404 para pegar um único objeto
#     card = get_object_or_404(
#         Card,
#         id=card_id,
#         publicado=True,
#         data_publicacao__isnull=False,
#         data_publicacao__lte=data_desejada,
#     )

#     context = {"card": card}  # card agora é um único objeto
#     return context


# @register.inclusion_tag("includes/topicos.html")
# def show_topicos():
#     topicos = Topico.objects.filter(atual=True)
#     hoje = date.today()

#     # Filtra os sub-tópicos
#     subtopicos = SubTopico.objects.filter(
#         publicado=True, data_publicacao__lte=hoje
#     ).order_by("-data_publicacao")[:6]

#     icones = [
#         "bi bi-briefcase",
#         "bi bi-card-checklist",
#         "bi bi-bar-chart",
#         "bi bi-binoculars",
#         "bi bi-brightness-high",
#         "bi bi-calendar4-week",
#     ]

#     # Associar ícones aos subtopicos
#     for i, subtopico in enumerate(subtopicos):
#         subtopico.icone = icones[i % len(icones)]  # Usar ícones de forma cíclica

#     context = {"topicos": topicos, "subtopicos": subtopicos}
#     return context


@register.inclusion_tag("includes/.html")
def show_():
    pass


@register.inclusion_tag("includes/footer.html")
def show_footer():
    return
