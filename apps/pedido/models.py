from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


from apps.produto.models import Produto


class Entregador(models.Model):
    nome = models.CharField(max_length=10)
    telefone = models.CharField(max_length=14, null=True, blank=True)
    vaiculo = models.CharField(max_length=50, null=True, blank=True)
    nome = models.CharField(max_length=10, unique=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Adm - Formas de Pagamento"
        verbose_name_plural = "Adm - Formas de Pagamento"

    def __str__(self):
        return self.nome

    placa = models.CharField(max_length=7, null=True, blank=True)
    data_cadastro = models.DateField(default=now)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Adm - Entregador"
        verbose_name_plural = "Adm - Entregador"

    def __str__(self):
        return self.nome


class FormaPagamento(models.Model):
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome


class Pedido(models.Model):
    data_pedido = models.DateTimeField(default=now)
    # cliente = models.ForeignKey(Cliente, on_delete=models.RESTRICT)
    usuario = models.ForeignKey(
        User, related_name="pedido_user", on_delete=models.PROTECT
    )
    forma_pagamento = models.ForeignKey(
        FormaPagamento, on_delete=models.RESTRICT, null=True
    )
    pago = models.BooleanField(default=False)
    # enviado = models.BooleanField(default=False)
    entregue = models.BooleanField(default=False)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    atendente = models.ForeignKey(User, on_delete=models.RESTRICT)
    entregador = models.ForeignKey(
        Entregador, on_delete=models.RESTRICT, null=True, blank=True
    )
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"(PEDIDO: {self.id})  CLIENTE: {self.usuario} - VALOR: {self.total} - DATA: {self.data_pedido.strftime('%d/%m/%y')}/ HORA: {self.data_pedido.strftime('%H:%M')}"

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedido"


# ItensPedido
class ItensCarrinho(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto = models.ForeignKey(
        Produto, related_name="produto", on_delete=models.CASCADE
    )
    quantidade = models.PositiveIntegerField(default=1)
    preco = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    # class Meta:
    #     verbose_name = "Itens do Carrinho"
    #     verbose_name_plural = "Itens do Carrinho"

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
