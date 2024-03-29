from rest_framework import serializers

from chat.models import Message, Chat, ChatMember


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('sender', 'text', 'dt_created')
        extra_kwargs = {
            'sender': {'read_only': True},
        }


class ChatMemberSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(source='user.profile.avatar')
    username = serializers.CharField(source='user.username')

    class Meta:
        model = ChatMember
        fields = ('username', 'user_id', 'avatar', 'write_access')


class ChatSerializer(serializers.ModelSerializer):
    initiator_name = serializers.CharField(source='initiator.username', read_only=True)

    class Meta:
        model = Chat
        fields = ('initiator_name', 'id')

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.add_member(user=self.context['request'].user)
        return instance


class ChatDetailSerializer(serializers.ModelSerializer):
    members = ChatMemberSerializer(source='chatmember_set', many=True)

    class Meta:
        model = Chat
        fields = ('initiator', 'id', 'members')
