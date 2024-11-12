from django.contrib import admin


from apps.pedido import models



admin.site.register(models.FormaPagamento)
class ItensCarrinhoInline(admin.TabularInline):
    model = models.ItensCarrinho
    readonly_fields = ("preco",)
    extra = 0


@admin.register(models.Pedido)
class PedidoAdmin(admin.ModelAdmin):
    fields = ("data_pedido", "usuario", "pagamento", "pago", "entregue")
    readonly_fields = ("usuario",)
    inlines = [
        ItensCarrinhoInline,
    ]
