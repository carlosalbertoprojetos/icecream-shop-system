from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.timezone import now


# py manage.py makemigrations && py manage.py migrate && py manage.py runserver


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
        verbose_name = "1 - Base"
        verbose_name_plural = "1 - Base"

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
        verbose_name = "2 - Produto"
        verbose_name_plural = "2 - Produto"

    def preco_formatado(self):
        return f"R$ {self.preco:.2f}"

    def __str__(self):
        return f"{self.base} {self.sabor} {self.preco_formatado()}"


class FormaPagamento(models.Model):
    nome = models.CharField(max_length=10, unique=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Adm - Formas de Pagamento"
        verbose_name_plural = "Adm - Formas de Pagamento"

    def __str__(self):
        return self.nome


class Entregador(models.Model):
    nome = models.CharField(max_length=10)
    telefone = models.CharField(max_length=14, null=True, blank=True)
    vaiculo = models.CharField(max_length=50, null=True, blank=True)
    placa = models.CharField(max_length=7, null=True, blank=True)
    data_cadastro = models.DateField(default=now)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Adm - Entregador"
        verbose_name_plural = "Adm - Entregador"

    def __str__(self):
        return self.nome


class Pedido(models.Model):
    data_pedido = models.DateTimeField(default=now)
    usuario = models.ForeignKey(
        User, related_name="pedido_user", on_delete=models.PROTECT
    )
    forma_pagamento = models.ForeignKey(
        FormaPagamento, on_delete=models.RESTRICT, null=True
    )
    pago = models.BooleanField(default=False)
    entregue = models.BooleanField(default=False)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    atendente = models.ForeignKey(User, on_delete=models.RESTRICT)
    entregador = models.ForeignKey(
        Entregador, on_delete=models.RESTRICT, null=True, blank=True
    )
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"PEDIDO: {self.id} _/  USUÁRIO: {self.user} _/  VALOR: {self.total} _/ PAGO: {self.pago} _/  DATA: {self.data_pedido.strftime('%d/%m/%y %H:%M')} _/ ENTREGADOR: {self.entregador}"

    class Meta:
        verbose_name = "3 - Pedido"
        verbose_name_plural = "3 - Pedido"


class ItensCarrinho(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto = models.ForeignKey(
        Produto, related_name="produto", on_delete=models.CASCADE
    )
    quantidade = models.PositiveIntegerField(default=1)
    preco = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    # class Meta:
    #     verbose_name = "3 - Itens do Carrinho"
    #     verbose_name_plural = "3 - Itens do Carrinho"

    def preco_formatado(self):
        return f"R$ {self.preco:.2f}"

    # calcula a soma dos preços de todos os produtos da sacola
    def preco_total(self):
        total = self.produto.preco * self.quantidade
        self.preco = total
        self.save()
        return total

    def __str__(self):
        return f"CARINHO: {self.quantidade} - {self.produto} / R$ {self.preco_total()}"
