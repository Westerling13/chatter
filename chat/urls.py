from django.urls import path

from chat.views import ChatListCreateView

urlpatterns = [
    path('', ChatListCreateView.as_view(), name='chat_list_create'),
]
