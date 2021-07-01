import channels.layers
from asgiref.sync import async_to_sync
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from chat.models import Chat, Message
from chat.serializers import ChatSerializer, MessageSerializer, ChatDetailSerializer, ChatMemberSerializer


class ChatListCreateView(generics.ListCreateAPIView):
    serializer_class = ChatSerializer
    queryset = Chat.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['initiator__username']

    def perform_create(self, serializer):
        serializer.save(initiator=self.request.user)

    def get(self, request, *args, **kwargs):
        """Список всех чатов."""
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Создание чата."""
        return self.create(request, *args, **kwargs)


class ChatDetailView(generics.RetrieveAPIView):
    serializer_class = ChatDetailSerializer
    lookup_url_kwarg = 'chat_id'

    def get_queryset(self):
        return Chat.objects.filter(chatmember__user=self.request.user)

    def get(self, request, *args, **kwargs):
        """Информация о чате."""
        return self.retrieve(request, *args, **kwargs)


class ChatMemberListCreateView(generics.GenericAPIView):
    serializer_class = ChatSerializer
    lookup_url_kwarg = 'chat_id'
    queryset = Chat.objects.all()

    def post(self, request, *args, **kwargs):
        """Присоединение к чату нового участника."""
        chat = self.get_object()
        if chat.members.filter(id=request.user.id).exists():
            raise ValidationError('Вы уже присоединились к этому чату.')

        chat.add_member(self.request.user)
        chat_member_serializer = ChatMemberSerializer(chat.chatmember_set.all(), many=True)
        return Response(chat_member_serializer.data, status=status.HTTP_201_CREATED)


class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        return Message.objects.filter(chat_id=self.kwargs['chat_id'])

    def perform_create(self, serializer):
        message = serializer.save(sender=self.request.user, chat_id=self.kwargs['chat_id'])
        chat_name = f'chat_{self.kwargs["chat_id"]}'
        channel_layer = channels.layers.get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            chat_name, {'type': 'chat_message', 'message': message.text},
        )

    def get(self, request, *args, **kwargs):
        """Список всех сообщений в чате."""
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Отправка нового сообщения в чат."""
        return self.create(request, *args, **kwargs)
