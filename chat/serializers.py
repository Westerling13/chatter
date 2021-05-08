from rest_framework import serializers

from chat.models import Message, Chat, ChatMember
from profiles.user import User


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('sender', 'text', 'dt_created')


class ChatMemberSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(source='profile.avatar')

    class Meta:
        model = User
        fields = ('username', 'id', 'avatar')


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ('initiator', 'id')

    def create(self, validated_data):
        instance = super().create(validated_data)
        ChatMember.objects.create(user=self.context['request'].user, chat=instance)

        return instance


class ChatDetailSerializer(serializers.ModelSerializer):
    members = ChatMemberSerializer(many=True)

    class Meta:
        model = Chat
        fields = ('initiator', 'id', 'members')
