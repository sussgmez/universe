from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _  
from django.dispatch import receiver
from django.db.models.signals import post_save


class Category(models.Model):
    name = models.CharField(_("Categoria"), max_length=100)

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey("Profile", verbose_name=_("Autor"), on_delete=models.CASCADE, related_name="post")
    content = models.TextField(_("Contenido"))
    category = models.ForeignKey(Category, verbose_name=_("Categoria"), on_delete=models.CASCADE, blank=True, null=True)
    commented = models.ForeignKey("self", verbose_name=_("Comentando"), on_delete=models.CASCADE, blank=True, null=True)
    created = models.DateTimeField(_("Fecha publicado"), auto_now_add=True)
    image = models.ImageField(_("Imagen"), upload_to='images/post', blank=True, null=True)

    class Meta:
        verbose_name = _("post")
        verbose_name_plural = _("posts")


class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name=_("Usuario"), on_delete=models.CASCADE)
    image = models.ImageField(_("Imagen"), upload_to='images/profile', blank=True, null=True)    
    description = models.CharField(_("Descripcion"), max_length=200, blank=True, null=True)
    liked_post = models.ManyToManyField(Post, verbose_name=_("Me gusta"), blank=True)
    following = models.ManyToManyField("self", verbose_name=_("Siguiendo"), blank=True, symmetrical=False)

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")


    def __str__(self):
        return f'profile_{self.user.username}'
    

@receiver(post_save, sender=User)
def user_post_save_receiver(sender, instance, created, **kwargs):
    if created:
        pf = Profile.objects.create(user=instance)
        pf.following.add(pf)
        pf.save()
