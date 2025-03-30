from django.db import models
from django.utils.translation import gettext_lazy as _  


class Chat(models.Model):
    profiles = models.ManyToManyField('authentication.Profile', verbose_name=_("Integrantes"), related_name='chats')

    def __str__(self):
        return f'Chat ID: {self.pk}'


class Message(models.Model):
    author = models.ForeignKey('authentication.Profile', verbose_name=_("Autor"), on_delete=models.CASCADE, related_name='messages')
    chat = models.ForeignKey(Chat, verbose_name=_("Chat"), on_delete=models.CASCADE, related_name='messages')
    content = models.TextField(_("Contenido"))
    created = models.DateTimeField(_("Fecha de envío"), auto_now_add=True)

    def __str__(self):
        return f'Message ID: {self.pk}'


