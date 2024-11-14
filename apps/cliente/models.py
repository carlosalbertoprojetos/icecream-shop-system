from django.contrib.auth.models import User
from django.db import models


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
