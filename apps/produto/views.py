from django.shortcuts import render
from .models import Produto


def listar_produtos(request):
    produtos = Produto.objects.filter(ativo=True)
    context = {
        "produtos": produtos,
    }
    return render(request, "menu.html", context)
