from django.contrib import admin

from chat.models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    raw_id_fields = ('sender', 'chat')
