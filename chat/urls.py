from django.urls import path

from chat.views import ChatListCreateView, ChatDetailView

urlpatterns = [
    path('', ChatListCreateView.as_view(), name='chat_list_create'),
    path('<int:chat_id>/', ChatDetailView.as_view(), name='chat_detail'),
]
