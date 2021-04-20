from rest_framework import serializers

from chat.models import Message, Chat, ChatMember


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('sender', 'text', 'dt_created')


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ('initiator', 'id')

    def create(self, validated_data):
        instance = super().create(validated_data)
        ChatMember.objects.create(user=self.context['request'].user, chat=instance)

        return instance
