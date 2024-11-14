from django.contrib import admin


from apps.produto import models as m


admin.site.register(m.TipoMercadoria)
admin.site.register(m.UnidadeMedida)
admin.site.register(m.Embalagem)
admin.site.register(m.Sabor)
admin.site.register(m.Base)
admin.site.register(m.Produto)
