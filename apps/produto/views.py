import csv
from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum, Count, Avg, F, Q
from django.utils import timezone
from django.http import HttpResponse
from django.core.paginator import Paginator



from .models import (
    Produto, Pedido, ItemPedido, StatusPedido, 
    HistoricoPedido, AvaliacaoPedido, Endereco
)
import csv
from django.http import HttpResponse
import datetime


def listar_produtos(request):
    produtos = Produto.objects.filter(ativo=True)
    context = {
        "produtos": produtos,
    }
    return render(request, "index.html", context)


# Função auxiliar para verificar se o usuário é administrador
def is_admin(user):
    return user.is_staff or user.is_superuser


# Dashboard administrativo
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    # Dados para o dashboard
    hoje = timezone.now().date()
    inicio_mes = hoje.replace(day=1)
    
    # Total de pedidos
    total_pedidos = Pedido.objects.count()
    pedidos_hoje = Pedido.objects.filter(data_criacao__date=hoje).count()
    pedidos_mes = Pedido.objects.filter(data_criacao__date__gte=inicio_mes).count()
    
    # Valor total de vendas
    total_vendas = Pedido.objects.aggregate(total=Sum('valor_total'))['total'] or 0
    vendas_hoje = Pedido.objects.filter(data_criacao__date=hoje).aggregate(total=Sum('valor_total'))['total'] or 0
    vendas_mes = Pedido.objects.filter(data_criacao__date__gte=inicio_mes).aggregate(total=Sum('valor_total'))['total'] or 0
    
    # Produtos mais vendidos
    produtos_populares = ItemPedido.objects.values('produto__sabor', 'produto__base__tipo__nome').annotate(
        total_vendido=Sum('quantidade')
    ).order_by('-total_vendido')[:5]
    
    # Status dos pedidos
    status_pedidos = Pedido.objects.values('status__nome').annotate(
        total=Count('id')
    ).order_by('status__nome')
    
    # Avaliações médias
    avaliacao_media = AvaliacaoPedido.objects.aggregate(media=Avg('nota'))['media'] or 0
    
    context = {
        'total_pedidos': total_pedidos,
        'pedidos_hoje': pedidos_hoje,
        'pedidos_mes': pedidos_mes,
        'total_vendas': total_vendas,
        'vendas_hoje': vendas_hoje,
        'vendas_mes': vendas_mes,
        'produtos_populares': produtos_populares,
        'status_pedidos': status_pedidos,
        'avaliacao_media': avaliacao_media,
    }
    
    return render(request, 'admin/dashboard.html', context)


# Relatório de pedidos
@login_required
@user_passes_test(is_admin)
def relatorio_pedidos(request):
    # Filtros
    status_id = request.GET.get('status')
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    
    pedidos = Pedido.objects.all().order_by('-data_criacao')
    
    if status_id:
        pedidos = pedidos.filter(status_id=status_id)
    
    if data_inicio:
        data_inicio = datetime.datetime.strptime(data_inicio, '%Y-%m-%d').date()
        pedidos = pedidos.filter(data_criacao__date__gte=data_inicio)
    
    if data_fim:
        data_fim = datetime.datetime.strptime(data_fim, '%Y-%m-%d').date()
        pedidos = pedidos.filter(data_criacao__date__lte=data_fim)
    
    # Paginação
    paginator = Paginator(pedidos, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Status para o filtro
    status_list = StatusPedido.objects.all()
    
    context = {
        'page_obj': page_obj,
        'status_list': status_list,
        'filtros': {
            'status_id': status_id,
            'data_inicio': data_inicio,
            'data_fim': data_fim,
        }
    }
    
    # Exportar para CSV
    if 'export' in request.GET:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="relatorio_pedidos.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Número', 'Cliente', 'Data', 'Status', 'Forma de Pagamento', 'Valor Total'])
        
        for pedido in pedidos:
            writer.writerow([
                pedido.numero,
                pedido.usuario.username,
                pedido.data_criacao.strftime('%d/%m/%Y %H:%M'),
                pedido.status.nome,
                pedido.get_forma_pagamento_display(),
                pedido.valor_total
            ])
        
        return response
    
    return render(request, 'admin/relatorio_pedidos.html', context)


# Relatório de vendas por período
@login_required
@user_passes_test(is_admin)
def relatorio_vendas(request):
    # Filtros
    periodo = request.GET.get('periodo', 'mensal')
    ano = request.GET.get('ano', timezone.now().year)
    
    # Dados para o gráfico
    dados_vendas = []
    
    if periodo == 'diario':
        # Últimos 30 dias
        data_fim = timezone.now().date()
        data_inicio = data_fim - timedelta(days=29)
        
        for i in range(30):
            data = data_inicio + timedelta(days=i)
            total = Pedido.objects.filter(
                data_criacao__date=data
            ).aggregate(total=Sum('valor_total'))['total'] or 0
            
            dados_vendas.append({
                'periodo': data.strftime('%d/%m'),
                'total': float(total)
            })
    
    elif periodo == 'mensal':
        # Meses do ano selecionado
        for mes in range(1, 13):
            total = Pedido.objects.filter(
                data_criacao__year=ano,
                data_criacao__month=mes
            ).aggregate(total=Sum('valor_total'))['total'] or 0
            
            dados_vendas.append({
                'periodo': datetime.date(int(ano), mes, 1).strftime('%b'),
                'total': float(total)
            })
    
    elif periodo == 'anual':
        # Últimos 5 anos
        ano_atual = timezone.now().year
        for i in range(5):
            ano_filtro = ano_atual - i
            total = Pedido.objects.filter(
                data_criacao__year=ano_filtro
            ).aggregate(total=Sum('valor_total'))['total'] or 0
            
            dados_vendas.append({
                'periodo': str(ano_filtro),
                'total': float(total)
            })
        
        dados_vendas.reverse()
    
    # Resumo
    total_geral = sum(item['total'] for item in dados_vendas)
    media = total_geral / len(dados_vendas) if dados_vendas else 0
    
    context = {
        'dados_vendas': dados_vendas,
        'periodo': periodo,
        'ano': ano,
        'anos_disponiveis': range(timezone.now().year - 4, timezone.now().year + 1),
        'total_geral': total_geral,
        'media': media
    }
    
    return render(request, 'admin/relatorio_vendas.html', context)

# Relatório de pedidos por cliente
@login_required
@user_passes_test(is_admin)
def relatorio_clientes(request):
    User = get_user_model()
    # Filtros
    busca = request.GET.get('busca', '')

    if busca:
        clientes = User.objects.filter(
            Q(email__icontains=busca) | Q(first_name__icontains=busca)            ).distinct()
    else:
        clientes = User.objects.filter(pedidos__isnull=False).distinct()

    # Dados dos clientes com estatísticas
    dados_clientes = []
    for cliente in clientes:
        pedidos = Pedido.objects.filter(usuario=cliente)
    
        dados_clientes.append({
            'id': cliente.id,
            'nome': f"{cliente.first_name} {cliente.last_name}".strip() or cliente.username,
            'email': cliente.email,
            'total_pedidos': pedidos.count(),
            'valor_total': pedidos.aggregate(total=Sum('valor_total'))['total'] or 0,
            'ultimo_pedido': pedidos.order_by('-data_criacao').first(),
            'ticket_medio': (pedidos.aggregate(total=Sum('valor_total'))['total'] or 0) / pedidos.count() if pedidos.count() > 0 else 0
        })

    # Ordenação
    ordem = request.GET.get('ordem', '-total_pedidos')
    if ordem == 'nome':
        dados_clientes.sort(key=lambda x: x['nome'])
    elif ordem == '-nome':
        dados_clientes.sort(key=lambda x: x['nome'], reverse=True)
    elif ordem == 'total_pedidos':
        dados_clientes.sort(key=lambda x: x['total_pedidos'])
    elif ordem == '-total_pedidos':
        dados_clientes.sort(key=lambda x: x['total_pedidos'], reverse=True)
    elif ordem == 'valor_total':
        dados_clientes.sort(key=lambda x: x['valor_total'])
    elif ordem == '-valor_total':
        dados_clientes.sort(key=lambda x: x['valor_total'], reverse=True)
    elif ordem == 'ticket_medio':
        dados_clientes.sort(key=lambda x: x['ticket_medio'])
    elif ordem == '-ticket_medio':
        dados_clientes.sort(key=lambda x: x['ticket_medio'], reverse=True)

    # Paginação
    paginator = Paginator(dados_clientes, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'busca': busca,
        'ordem': ordem
    }

    # Exportar para CSV
    if 'export' in request.GET:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="relatorio_clientes.csv"'
    
        writer = csv.writer(response)
        writer.writerow(['Nome', 'Email', 'Total de Pedidos', 'Valor Total', 'Ticket Médio', 'Data Último Pedido'])
    
        for cliente in dados_clientes:
            writer.writerow([
                cliente['nome'],
                cliente['email'],
                cliente['total_pedidos'],
                cliente['valor_total'],
                cliente['ticket_medio'],
                cliente['ultimo_pedido'].data_criacao.strftime('%d/%m/%Y %H:%M') if cliente['ultimo_pedido'] else 'N/A'
            ])
    
        return response

    return render(request, 'admin/relatorio_clientes.html', context)