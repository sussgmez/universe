from django.db import models
from django.utils.translation import gettext_lazy as _  


class Category(models.Model):
    name = models.CharField(_("Categoria"), max_length=100)

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __str__(self):
        return self.name


class Publication(models.Model):
    author = models.ForeignKey("authentication.Profile", verbose_name=_("Autor"), on_delete=models.CASCADE, related_name="publication")
    content = models.TextField(_("Contenido"))
    category = models.ForeignKey(Category, verbose_name=_("Categoria"), on_delete=models.CASCADE, blank=True, null=True)
    commented = models.ForeignKey("self", verbose_name=_("Comentando"), on_delete=models.CASCADE, blank=True, null=True)
    created = models.DateTimeField(_("Fecha publicado"), auto_now_add=True)
    image = models.ImageField(_("Imagen"), upload_to='images/publication', blank=True, null=True)

