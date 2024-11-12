from django.contrib import admin
from .models import Cliente, Endereco


# admin.site.register(models.FormaPagamento)

# admin.site.register(models.ItensCarrinho)


# @admin.register(models.ItensCarrinho)
# class ItensCarrinhoAdmin(admin.ModelAdmin):
#     readonly_fields = ("preco",)


class EnderecoInline(admin.TabularInline):
    model = Endereco
    # readonly_fields = ("preco",)
    # extra = 0


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    fields = ("usuario", "cpf", "data_nascimento", "email")
    # readonly_fields = ("user",)
    inlines = [
        EnderecoInline,
    ]
