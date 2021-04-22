from django.urls import path

from chat.views import ChatListCreateView, ChatDetailView, MessageListCreateView

urlpatterns = [
    path('', ChatListCreateView.as_view(), name='chat_list_create'),
    path('<int:chat_id>/', ChatDetailView.as_view(), name='chat_detail'),
    path('<int:chat_id>/messages/', MessageListCreateView.as_view(), name='message_list_create'),
]
