from django.contrib import admin

from chat.models import Message, Chat


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    raw_id_fields = ('sender', 'chat')


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    raw_id_fields = ('initiator',)
