from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid


# Tipo de mercadoria que será comercialiaca, ex: Picolé, Açaí, Sorvete, Chocolate, Biscoito
class TipoMercadoria(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Adm - Tipo de Mercadoria"
        verbose_name_plural = "Adm - Tipo de Mercadoria"

    def __str__(self):
        return self.nome


# Unidade, litro, quilo, m³, etc
class UnidadeMedida(models.Model):
    um = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Adm - Unidade de Medida"
        verbose_name_plural = "Adm - Unidade de Medida"

    def __str__(self):
        return self.um


# Tipo da embalagem de armazenamento do produto (1L - 1/5L - 2L - 400mL - 800mL )
class Embalagem(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Adm - Embalagem"
        verbose_name_plural = "Adm - Embalagem"

    def __str__(self):
        return self.nome


# Sabores ofertados (morango, chocolate, diamante negro, laka, etc)
class Sabor(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Adm - Sabor"
        verbose_name_plural = "Adm - Sabor"

    def __str__(self):
        return f"{self.nome}"


# base para a criação do produto
# exemplo: Picolé, unidade, palito ou Sorvete, litro, pote 3Litros ou Açaí, litro, pote 400ml
class Base(models.Model):
    tipo = models.ForeignKey(TipoMercadoria, on_delete=models.CASCADE)
    um = models.ForeignKey(UnidadeMedida, on_delete=models.RESTRICT)
    embalagem = models.ForeignKey(Embalagem, on_delete=models.RESTRICT)
    ativo = models.BooleanField(default=True)

    class Meta:
        unique_together = (("tipo", "um", "embalagem"),)
        verbose_name = "Base"
        verbose_name_plural = "Base"

    def __str__(self):
        return f"{self.tipo} {self.embalagem}"


class Produto(models.Model):
    base = models.ForeignKey(Base, on_delete=models.RESTRICT)
    sabor = models.ForeignKey(Sabor, on_delete=models.RESTRICT)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    imagem = models.ImageField(upload_to="media")
    descricao = models.CharField(max_length=255, null=True, blank=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        unique_together = (("base", "sabor", "preco"),)
        verbose_name = "Produto"
        verbose_name_plural = "Produto"

    def preco_formatado(self):
        return f"R$ {self.preco:.2f}"

    def __str__(self):
        return f"{self.base} {self.sabor} {self.preco_formatado()}"


# Novo modelo para endereço de entrega
class Endereco(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enderecos')
    cep = models.CharField(max_length=9)
    logradouro = models.CharField(max_length=255)
    numero = models.CharField(max_length=20)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    padrao = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Endereço"
        verbose_name_plural = "Endereços"
    
    def __str__(self):
        return f"{self.logradouro}, {self.numero} - {self.bairro}, {self.cidade}/{self.estado}"


# Status do pedido
class StatusPedido(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    descricao = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Status do Pedido"
        verbose_name_plural = "Status dos Pedidos"
    
    def __str__(self):
        return self.nome


# Pedido
class Pedido(models.Model):
    FORMA_PAGAMENTO_CHOICES = [
        ('cartao', 'Cartão de Crédito/Débito'),
        ('pix', 'PIX'),
        ('dinheiro', 'Dinheiro'),
    ]
    
    numero = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pedidos')
    endereco_entrega = models.ForeignKey(Endereco, on_delete=models.PROTECT)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_modificacao = models.DateTimeField(auto_now=True)
    status = models.ForeignKey(StatusPedido, on_delete=models.PROTECT)
    forma_pagamento = models.CharField(max_length=20, choices=FORMA_PAGAMENTO_CHOICES)
    valor_produtos = models.DecimalField(max_digits=10, decimal_places=2)
    valor_frete = models.DecimalField(max_digits=10, decimal_places=2)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    observacoes = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-data_criacao']
    
    def __str__(self):
        return f"Pedido #{self.numero} - {self.usuario.username}"
    
    def calcular_total(self):
        self.valor_produtos = sum(item.subtotal for item in self.itens.all())
        self.valor_total = self.valor_produtos + self.valor_frete
        self.save()


# Item do pedido
class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.PositiveIntegerField(default=1)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = "Item do Pedido"
        verbose_name_plural = "Itens do Pedido"
    
    def __str__(self):
        return f"{self.quantidade}x {self.produto.sabor} - {self.pedido.numero}"
    
    def save(self, *args, **kwargs):
        self.preco_unitario = self.produto.preco
        self.subtotal = self.quantidade * self.preco_unitario
        super().save(*args, **kwargs)
        self.pedido.calcular_total()


# Histórico de status do pedido
class HistoricoPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='historico')
    status = models.ForeignKey(StatusPedido, on_delete=models.PROTECT)
    data = models.DateTimeField(auto_now_add=True)
    observacao = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Histórico do Pedido"
        verbose_name_plural = "Histórico dos Pedidos"
        ordering = ['-data']
    
    def __str__(self):
        return f"{self.pedido.numero} - {self.status.nome} em {self.data.strftime('%d/%m/%Y %H:%M')}"


# Avaliação do pedido
class AvaliacaoPedido(models.Model):
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE, related_name='avaliacao')
    nota = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    comentario = models.TextField(blank=True, null=True)
    data = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Avaliação do Pedido"
        verbose_name_plural = "Avaliações dos Pedidos"
    
    def __str__(self):
        return f"Avaliação do Pedido {self.pedido.numero} - Nota: {self.nota}"