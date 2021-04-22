from rest_framework import generics

from chat.models import Chat
from chat.serializers import ChatSerializer


class ChatListCreateView(generics.ListCreateAPIView):
    serializer_class = ChatSerializer
    queryset = Chat.objects

    def perform_create(self, serializer):
        serializer.save(initiator=self.request.user)


class ChatDetailView(generics.RetrieveAPIView):
    serializer_class = ChatSerializer
    lookup_url_kwarg = 'chat_id'

    def get_queryset(self):
        return Chat.objects.filter(chatmember__user=self.request.user)
