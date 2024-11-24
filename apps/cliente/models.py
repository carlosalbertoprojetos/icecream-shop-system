from django.contrib.auth.models import User
from django.db import models

from apps.produto.models import Produto
from core import settings


class Cliente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    cpf = models.CharField(max_length=14, unique=True, null=True, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    telefone = models.CharField(max_length=15, null=True, blank=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.usuario.username


class Endereco(models.Model):
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE)
    cep = models.CharField(max_length=10)
    logradouro = models.CharField(max_length=100)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    numero = models.CharField(max_length=10, blank=True)
    complemento = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.logradouro}, {self.numero} - {self.bairro}, {self.cidade}"


class Carrinho(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, blank=True)
    produtos = models.ManyToManyField(Produto, blank=True)
    total = models.DecimalField(default=0.00, max_digits=15, decimal_places=2)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Carrinho"

    def __str__(self):
        return str(self.id)


# class ItensCarrinho(models.Model):
#     produto = models.ForeignKey(
#         Produto, related_name="produto", on_delete=models.CASCADE
#     )
#     quantidade = models.PositiveIntegerField(default=1)
#     preco = models.DecimalField(max_digits=10, decimal_places=2, null=True)

#     # class Meta:
#     #     verbose_name = "Itens do Carrinho"
#     #     verbose_name_plural = "Itens do Carrinho"

#     def preco_formatado(self):
#         return f"R$ {self.preco:.2f}"

#     # calcula a soma dos preços de todos os produtos da sacola
#     def preco_total(self):
#         total = self.produto.preco * self.quantidade
#         self.preco = total
#         self.save()
#         return total

#     def __str__(self):
#         return f"CARINHO: {self.quantidade} - {self.produto} / R$ {self.preco_total()}"
