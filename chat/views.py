from rest_framework import generics
from rest_framework.filters import SearchFilter

from chat.models import Chat, Message
from chat.serializers import ChatSerializer, MessageSerializer, ChatDetailSerializer


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


class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        return Message.objects.filter(chat_id=self.kwargs['chat_id'])

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user, chat_id=self.kwargs['chat_id'])
