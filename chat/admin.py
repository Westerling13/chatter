from django.contrib import admin

from chat.models import Message, Chat, Attachment


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    raw_id_fields = ('sender', 'chat')


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    raw_id_fields = ('initiator',)


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    raw_id_fields = ('message',)
