from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
import requests


from .forms import ClienteForm, EnderecoForm
from apps.pedido.models import Pedido


def clienteCadastro(request):
    if request.method == "POST":
        cliente_form = ClienteForm(request.POST)
        endereco_form = EnderecoForm(request.POST)

        if cliente_form.is_valid() and endereco_form.is_valid():
            cliente = cliente_form.save()
            endereco = endereco_form.save(commit=False)
            endereco.cliente = cliente
            endereco.save()

            # Logar automaticamente
            user = authenticate(
                username=cliente.usuario.username,
                password=cliente_form.cleaned_data["password"],
            )
            login(request, user)

            # Enviar email com senha
            send_mail(
                "Bem-vindo! Aqui está sua senha",
                f'Olá, {cliente.usuario.username}, sua senha é: {cliente_form.cleaned_data["password"]}',
                "admin@seusite.com",
                [cliente.usuario.email],
            )

            return redirect(
                "pagina_inicial"
            )  # Redirecionar para a página principal após o registro

    else:
        cliente_form = ClienteForm()
        endereco_form = EnderecoForm()
    template_name = "cliente/clienteCadastro.html"
    return render(
        request,
        template_name,
        {"cliente_form": cliente_form, "endereco_form": endereco_form},
    )


# View para buscar endereço a partir do CEP
def busca_cep(request):
    cep = request.GET.get("cep")
    response = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
    data = response.json()

    return JsonResponse(data)







# # lista os pedidos do usuário
@login_required(login_url="/admin/login/")
def meus_pedidos(request):
    if request.user.is_staff:
        meus_pedidos = Pedido.objects.all()
    else:
        meus_pedidos = Pedido.objects.filter(user=request.user)
    return render(request, "meus-pedidos.html", {"meus_pedidos": meus_pedidos})