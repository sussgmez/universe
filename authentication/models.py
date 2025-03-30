from django.db import models
from django.utils.translation import gettext_lazy as _  
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name=_("Usuario"), on_delete=models.CASCADE)
    image = models.ImageField(_("Imagen"), upload_to='images/profile', blank=True, null=True)    
    description = models.CharField(_("Descripción"), max_length=200, blank=True, null=True)
    liked_publications = models.ManyToManyField("publications.Publication", verbose_name=_("Me gustas"), blank=True)
    following = models.ManyToManyField("self", verbose_name=_("Siguiendo"), blank=True, symmetrical=False)

    def __str__(self):
        return f'Profile ID: {self.pk}, user: {self.user.username}'
    
@receiver(post_save, sender=User)
def user_post_save_receiver(sender, instance, created, **kwargs):
    if created:
        pf = Profile.objects.create(pk=instance.pk, user=instance)
        pf.following.add(pf)
        pf.description = ''
        pf.save()
