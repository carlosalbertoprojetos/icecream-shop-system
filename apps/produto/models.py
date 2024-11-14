from django.db import models


# Tipo de mercadoria que será comercialiaca, ex: Picolé, Açaí, Sorvete, Chocolate, Biscoito
class TipoMercadoria(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Adm - Tipo de Mercadoria"
        verbose_name_plural = "Adm - Tipo de Mercadoria"

    def __str__(self):
        return self.nome


# Unidade, litro, quilo, m³, etc
class UnidadeMedida(models.Model):
    um = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Adm - Unidade de Medida"
        verbose_name_plural = "Adm - Unidade de Medida"

    def __str__(self):
        return self.um


# Tipo da embalagem de armazenamento do produto (1L - 1/5L - 2L - 400mL - 800mL )
class Embalagem(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Adm - Embalagem"
        verbose_name_plural = "Adm - Embalagem"

    def __str__(self):
        return self.nome


# Sabores ofertados (morango, chocolate, diamante negro, laka, etc)
class Sabor(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Adm - Sabor"
        verbose_name_plural = "Adm - Sabor"

    def __str__(self):
        return f"{self.nome}"


# base para a criação do produto
# exemplo: Picolé, unidade, palito ou Sorvete, litro, pote 3Litros ou Açaí, litro, pote 400ml
class Base(models.Model):
    tipo = models.ForeignKey(TipoMercadoria, on_delete=models.CASCADE)
    um = models.ForeignKey(UnidadeMedida, on_delete=models.RESTRICT)
    embalagem = models.ForeignKey(Embalagem, on_delete=models.RESTRICT)
    ativo = models.BooleanField(default=True)

    class Meta:
        unique_together = (("tipo", "um", "embalagem"),)
        verbose_name = "Base"
        verbose_name_plural = "Base"

    def __str__(self):
        return f"{self.tipo} {self.embalagem}"


class Produto(models.Model):
    base = models.ForeignKey(Base, on_delete=models.RESTRICT)
    sabor = models.ForeignKey(Sabor, on_delete=models.RESTRICT)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    imagem = models.ImageField(upload_to="media")
    descricao = models.CharField(max_length=255, null=True, blank=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        unique_together = (("base", "sabor", "preco"),)
        verbose_name = "Produto"
        verbose_name_plural = "Produto"

    def preco_formatado(self):
        return f"R$ {self.preco:.2f}"

    def __str__(self):
        return f"{self.base} {self.sabor} {self.preco_formatado()}"
