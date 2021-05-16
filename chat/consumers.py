from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer


class ChatConsumer(JsonWebsocketConsumer):
    def connect(self):
        if self.scope['user'].is_anonymous:
            self.close()

        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat_name = f'chat_{self.chat_id}'

        async_to_sync(self.channel_layer.group_add)(self.chat_name, self.channel_name)
        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(self.chat_name, self.channel_name)

    def chat_message(self, event):
        self.send_json({'message': event['message']})
