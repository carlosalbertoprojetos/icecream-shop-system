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



# import pandas as pd
# from collections import Counter

# def analisar_sorteios(sorteios):
#     total_sorteios = len(sorteios)
#     posicao_contagem = [Counter() for _ in range(15)]
#     numero_contagem = Counter()
    
#     for sorteio in sorteios:
#         for i, numero in enumerate(sorteio):
#             posicao_contagem[i][numero] += 1
#             numero_contagem[numero] += 1
    
#     probabilidades_posicao = []
#     for i, contagem in enumerate(posicao_contagem):
#         total_posicao = sum(contagem.values())
#         probabilidades_posicao.append({num: cont / total_posicao for num, cont in contagem.items()})
    
#     probabilidades_geral = {num: cont / total_sorteios for num, cont in numero_contagem.items()}
    
#     return probabilidades_posicao, probabilidades_geral

# def carregar_sorteios_excel(arquivo):
#     df = pd.read_excel(arquivo, header=None)
#     sorteios = df.iloc[7:, 2:].values.tolist()
#     sorteios = [list(map(int, filter(lambda x: pd.notna(x), linha))) for linha in sorteios]
#     return sorteios

# # Exemplo de uso
# arquivo_excel = "sorteios.xlsx"
# sorteios_passados = carregar_sorteios_excel(arquivo_excel)
# prob_posicao, prob_geral = analisar_sorteios(sorteios_passados)

# print("Probabilidades por posição:")
# for i, probs in enumerate(prob_posicao):
#     print(f"Posição {i+1}: {probs}")

# print("\nProbabilidades gerais:")
# print(prob_geral)


# import pandas as pd
# from collections import Counter
# import streamlit as st

# def analisar_sorteios(sorteios):
#     total_sorteios = len(sorteios)
#     posicao_contagem = [Counter() for _ in range(15)]
#     numero_contagem = Counter()
    
#     for sorteio in sorteios:
#         for i, numero in enumerate(sorteio):
#             posicao_contagem[i][numero] += 1
#             numero_contagem[numero] += 1
    
#     probabilidades_posicao = []
#     for i, contagem in enumerate(posicao_contagem):
#         total_posicao = sum(contagem.values())
#         probabilidades_posicao.append({num: cont / total_posicao for num, cont in contagem.items()})
    
#     probabilidades_geral = {num: cont / total_sorteios for num, cont in numero_contagem.items()}
    
#     return probabilidades_posicao, probabilidades_geral

# def carregar_sorteios_excel(arquivo):
#     df = pd.read_excel(arquivo, header=None)
#     sorteios = df.iloc[7:, 2:].values.tolist()
#     sorteios = [list(map(int, filter(lambda x: pd.notna(x), linha))) for linha in sorteios]
#     return sorteios

# st.title("Análise de Sorteios")

# uploaded_file = st.file_uploader("Envie o arquivo Excel (.xlsx)", type=["xlsx"])

# if uploaded_file:
#     sorteios_passados = carregar_sorteios_excel(uploaded_file)
#     prob_posicao, prob_geral = analisar_sorteios(sorteios_passados)
    
#     st.subheader("Probabilidades por posição:")
#     for i, probs in enumerate(prob_posicao):
#         st.write(f"Posição {i+1}: {probs}")
    
#     st.subheader("Probabilidades gerais:")
#     st.write(prob_geral)


# import pandas as pd
# from collections import Counter
# import streamlit as st

# def analisar_sorteios(sorteios):
#     total_sorteios = len(sorteios)
#     posicao_contagem = [Counter() for _ in range(15)]
#     numero_contagem = Counter()

#     for sorteio in sorteios:
#         for i, numero in enumerate(sorteio):
#             posicao_contagem[i][numero] += 1
#             numero_contagem[numero] += 1

#     probabilidades_posicao = []
#     for i, contagem in enumerate(posicao_contagem):
#         total_posicao = sum(contagem.values())
#         probabilidades_posicao.append({num: cont / total_posicao for num, cont in contagem.items()})

#     probabilidades_geral = {num: cont / total_sorteios for num, cont in numero_contagem.items()}

#     return probabilidades_posicao, probabilidades_geral

# def carregar_sorteios_excel(arquivo):
#     df = pd.read_excel(arquivo, header=None)
#     sorteios = df.iloc[7:, 2:].values.tolist()
#     sorteios = [list(map(int, filter(lambda x: pd.notna(x), linha))) for linha in sorteios]
#     return sorteios

# st.title("Análise de Sorteios")

# uploaded_file = st.file_uploader("Envie o arquivo Excel (.xlsx)", type=["xlsx"])

# if uploaded_file:
#     sorteios_passados = carregar_sorteios_excel(uploaded_file)
#     prob_posicao, prob_geral = analisar_sorteios(sorteios_passados)
    
#     st.subheader("Probabilidades por posição:")
#     for i, probs in enumerate(prob_posicao):
#         st.write(f"Posição {i+1}: {probs}")
    
#     st.subheader("Probabilidades gerais:")
#     st.write(prob_geral)


# views.py
import pandas as pd
from collections import Counter


def process_lottery_data(file):
    # Lê a planilha a partir da 8ª linha (skiprows=7) e da 3ª coluna (usecols=[2, 3, ..., 16])
    df = pd.read_excel(file, skiprows=7, usecols=range(2, 17))
    
    # Garante que há pelo menos 15 colunas (para 15 números sorteados por vez)
    if df.shape[1] < 15:
        return {"error": "O arquivo deve conter pelo menos 15 colunas para os números sorteados."}
    
    # Contadores gerais
    total_count = Counter()
    position_count = [Counter() for _ in range(15)]
    total_draws = len(df)
    
    for _, row in df.iterrows():
        numbers = row[:15].tolist()
        for pos, num in enumerate(numbers):
            total_count[num] += 1
            position_count[pos][num] += 1
    
    # Probabilidades gerais
    probability_data = {num: round(count / total_draws, 4) for num, count in total_count.items()}
    
    # Números mais sorteados por posição
    position_results = [{
        "position": i+1,
        "most_frequent": max(pos_counter, key=pos_counter.get),
        "count": max(pos_counter.values())
    } for i, pos_counter in enumerate(position_count)]
    
    # Ordena os números pela maior probabilidade (do maior para o menor)
    sorted_probabilities = sorted(probability_data.items(), key=lambda x: x[1], reverse=True)
    
    # Obtém os 15 números com as maiores probabilidades
    top_15_numbers = [num for num, _ in sorted_probabilities[:15]]
    
    return {
        "probabilities": probability_data,
        "position_results": position_results,
        "top_15_numbers": top_15_numbers
    }


def upload_lottery_results(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        result = process_lottery_data(file)
        if "error" in result:
            return JsonResponse(result, status=400)
        return render(request, 'cliente/results.html', result)
    
    return render(request, 'cliente/upload.html')
