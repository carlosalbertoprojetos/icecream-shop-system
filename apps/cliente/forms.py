from django import forms
from django.contrib.auth.models import User
from .models import Cliente, Endereco


class ClienteForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Cliente
        fields = ["username", "cpf", "data_nascimento"]

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data["username"],
            password=self.cleaned_data["password"],
            email=self.cleaned_data["email"],
        )
        cliente = Cliente(
            usuario=user,
            cpf=self.cleaned_data["cpf"],
            data_nascimento=self.cleaned_data["data_nascimento"],
        )
        if commit:
            cliente.save()
        return cliente


class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = [
            "cep",
            "logradouro",
            "bairro",
            "cidade",
            "estado",
            "numero",
            "complemento",
        ]
