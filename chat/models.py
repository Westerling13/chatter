import os

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

    def add_member(self, user):
        return ChatMember.objects.create(user=user, chat=self)


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


def path_to_attachment(instance, filename):
    return os.path.join('chats', str(instance.message.chat_id), filename)


def path_to_attachment_preview(instance, filename):
    return os.path.join('chats', 'previews', str(instance.message.chat_id), filename)


class Attachment(AutoDateMixin):
    message = models.ForeignKey(Message, verbose_name='Сообщение', on_delete=models.CASCADE)
    file = models.FileField('Файл', upload_to=path_to_attachment)
    preview = models.ImageField('Превью для изображений', upload_to=path_to_attachment_preview, null=True, blank=True)
    is_image = models.BooleanField('Изображение', default=False)
    original_name = models.CharField('Оригинальное имя файла', max_length=50)

    class Meta:
        verbose_name = 'Вложение'
        verbose_name_plural = 'Вложения'

    def __str__(self):
        return f'Attachment#{self.id}'
