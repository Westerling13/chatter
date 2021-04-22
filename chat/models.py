from django.db import models

from common_utils.mixins import AutoDateMixin
from profiles.user import User


class ChatMember(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.SET_NULL, null=True, blank=True)
    chat = models.ForeignKey('Chat', on_delete=models.SET_NULL, null=True, blank=True)
    write_access = models.BooleanField('Право на отправку сообщений', default=True)


class Chat(AutoDateMixin):
    members = models.ManyToManyField(User, verbose_name='Участники чата', through=ChatMember)
    initiator = models.ForeignKey(
        User, verbose_name='Создатель чата', related_name='chats', on_delete=models.SET_NULL, null=True, blank=True,
    )

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'

    def __str__(self):
        return f'Чат#{self.id}'


class Message(AutoDateMixin):
    sender = models.ForeignKey(
        User,
        verbose_name='Отправитель',
        related_name='sent_messages',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    text = models.TextField('Текст сообщения')
    chat = models.ForeignKey('Chat', verbose_name='Чат', on_delete=models.CASCADE, related_name='messages')
    read_marks = models.ManyToManyField(User, verbose_name='Отметки о прочтении', related_name='read_marks')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return f'Сообщение#{self.id}'
