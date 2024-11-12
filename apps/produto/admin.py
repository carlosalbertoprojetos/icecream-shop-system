from django.contrib import admin


from apps.produto import models



admin.site.register(models.TipoMercadoria)
admin.site.register(models.UnidadeMedida)
admin.site.register(models.Embalagem)
admin.site.register(models.Sabor)
admin.site.register(models.Produto)
