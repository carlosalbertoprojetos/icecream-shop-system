from django.contrib import admin
from apps.base import models

# Registre seus modelos aqui

# admin.site.register(models.Cobertura)


admin.site.register(models.Entregador)


# admin.site.register(models.ItensCarrinho)


# @admin.register(models.ItensCarrinho)
# class ItensCarrinhoAdmin(admin.ModelAdmin):
#     readonly_fields = ("preco",)

# admin.site.register(models.FormaPagamento)
# class ItensCarrinhoInline(admin.TabularInline):
#     model = models.ItensCarrinho
#     readonly_fields = ("preco",)
#     extra = 0


# @admin.register(models.Pedido)
# class PedidoAdmin(admin.ModelAdmin):
#     fields = ("data_pedido", "usuario", "pagamento", "pago", "entregue")
#     readonly_fields = ("usuario",)
#     inlines = [
#         ItensCarrinhoInline,
#     ]


# Sabor
# class ProdutoAdmin(admin.ModelAdmin):
#     model = models.Produto


# Monta Pote
# class SelCoberturaInline(admin.TabularInline):
#     model = models.SelCobertura
#     extra = 0


# class SelSaborInline(admin.TabularInline):
#     model = models.SelSabor
#     extra = 0


# @admin.register(models.MontaPote)
# class MontaPoteAdmin(admin.ModelAdmin):
#     inlines = [SelSaborInline, SelCoberturaInline]


# # Sacola de Itens
# class MontaPoteInline(admin.TabularInline):
#     model = models.SacolaItens.potes.through
#     extra = 0


# class PedidoInline(admin.StackedInline):
#     model = models.Pedido
#     readonly_fields = ("user",)
#     extra = 0


# @admin.register(models.SacolaItens)
# class SacolaItensAdmin(admin.ModelAdmin):
#     fields = ("preco",)
#     readonly_fields = ("preco",)
#     inlines = [PedidoInline, MontaPoteInline]
