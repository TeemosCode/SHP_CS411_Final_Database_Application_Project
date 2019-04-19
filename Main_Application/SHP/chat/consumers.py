from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from .models import Message

User = get_user_model()

# chat/consumers.py


class ChatConsumer(WebsocketConsumer):

    def message_to_json(self, message):
        return {
            'author': message.author.username,
            'content': message.content,
            'timestamp': str(message.timestamp)
        }

    def messages_to_json(self, messages):
        return [self.message_to_json(message) for message in messages]

    def fetch_messages(self, data):
        print('fetch message')
        messages = Message.last_10_messages()
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages),
        }
        print(content)
        self.send_chat_message(content)

    def new_message(self, data):
        print('new message created')
        author = data['from']
        author_user = User.objects.filter(username=author)[0]
        message = Message.objects.create(
            author=author_user, content=data['message']
        )
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

    def connect(self):  # Adding user to the group
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):  # Getting input message data
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_chat_message(self, message):

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    # Receive message from room group
    def chat_message(self, event):  # Send command
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps(message))
