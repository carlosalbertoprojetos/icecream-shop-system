from django.contrib import admin


from apps.pedido import models


admin.site.register(models.FormaPagamento)


# class ItensCarrinhoInline(admin.TabularInline):
#     model = models.ItensCarrinho
#     readonly_fields = ("preco",)
#     extra = 0


# @admin.register(models.Pedido)
# class PedidoAdmin(admin.ModelAdmin):
#     fields = (
#         "data_pedido",
#         "usuario",
#         "forma_pagamento",
#         "pago",
#         "entregue",
#     )
#     readonly_fields = ("usuario",)
#     list_display = (
#         "data_pedido_id",
#         "usuario",
#         "atendente",
#         "forma_pagamento",
#         "pago",
#         "entregue",
#     )
#     inlines = [
#         ItensCarrinhoInline,
#     ]

#     def data_pedido_id(self, obj):
#         return f"{obj.data_pedido.strftime('%d/%m/%y')} - {obj.id}"

#     data_pedido_id.short_description = "Data do Pedido"

#     def save_model(self, request, obj, form, change):
#         # Atribui o usuário logado ao campo `atendente` e `usuario` somente se for um novo registro
#         if not change:
#             obj.atendente = request.user
#             obj.usuario = request.user
#         super().save_model(request, obj, form, change)


from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from . import models


class ItensCarrinhoInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        # Verifica se existe pelo menos um item no carrinho
        if not any(
            form.cleaned_data and not form.cleaned_data.get("DELETE", False)
            for form in self.forms
        ):
            raise ValidationError(
                "O pedido deve conter pelo menos um item no carrinho."
            )


class ItensCarrinhoInline(admin.TabularInline):
    model = models.ItensCarrinho
    formset = ItensCarrinhoInlineFormSet
    readonly_fields = ("preco",)
    extra = 0


@admin.register(models.Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = (
        "data_pedido_id",
        "usuario",
        "atendente",
        "forma_pagamento",
        "pago",
        "entregue",
    )
    fields = (
        "data_pedido",
        "usuario",
        "atendente",
        "forma_pagamento",
        "pago",
        "entregue",
    )
    readonly_fields = ("usuario",)
    inlines = [ItensCarrinhoInline]

    def data_pedido_id(self, obj):
        return f"{obj.data_pedido.strftime('%d/%m/%y')} - {obj.id}"

    data_pedido_id.short_description = "Data do Pedido"

    def save_model(self, request, obj, form, change):
        if not change:
            obj.usuario = request.user
            obj.atendente = request.user
        super().save_model(request, obj, form, change)
