from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.timezone import now


from apps.base.models import Entregador
from apps.produto.models import Produto


class FormaPagamento(models.Model):
    nome = models.CharField(max_length=255)

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
        return f"(PEDIDO: {self.id})  CLIENTE: {self.usuario} - VALOR: {self.total} - DATA: {self.data_pedido.strftime('%d/%m/%y')}/ HORA: {self.data_pedido.strftime('%H:%M')}"

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedido"


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
