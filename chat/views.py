from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from chat.models import Chat, Message
from chat.serializers import ChatSerializer, MessageSerializer, ChatDetailSerializer, ChatMemberSerializer


class ChatListCreateView(generics.ListCreateAPIView):
    serializer_class = ChatSerializer
    queryset = Chat.objects
    filter_backends = [SearchFilter]
    search_fields = ['initiator__username']

    def perform_create(self, serializer):
        serializer.save(initiator=self.request.user)


class ChatDetailView(generics.RetrieveAPIView):
    serializer_class = ChatDetailSerializer
    lookup_url_kwarg = 'chat_id'

    def get_queryset(self):
        return Chat.objects.filter(chatmember__user=self.request.user)


class ChatMemberListCreateView(generics.GenericAPIView):
    serializer_class = ChatSerializer
    lookup_url_kwarg = 'chat_id'
    queryset = Chat.objects.all()

    def post(self, request, *args, **kwargs):
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
        serializer.save(sender=self.request.user, chat_id=self.kwargs['chat_id'])
