from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from .models import Message
from django.db import connection

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
        print(data)
        chatroom_id = data['chatroomid']
        with connection.cursor() as cursor:
            get_all_historical_chat_ascending_query = """
                SELECT * FROM PrivateChatHistory
                WHERE chatroomid = %s
                ORDER BY messagetime ASC;
            """

            cursor.execute(get_all_historical_chat_ascending_query, [chatroom_id])
            chat_history_rows = cursor.fetchall()

            get_chatroom_user_names_query = """
                SELECT B.userid, B.username, B2.userid, B2.username
                FROM PrivateChatRoom AS P 
                JOIN BUser AS B ON P.member1id = B.userid 
                JOIN BUser AS B2 ON P.member2id = B2.userid;
            """
            cursor.execute(get_chatroom_user_names_query)
            chatroom_id_to_username = cursor.fetchone()
            userid_to_username_map = {
                chatroom_id_to_username[0]: chatroom_id_to_username[1],
                chatroom_id_to_username[2]: chatroom_id_to_username[3]
            }
            # print(chat_history_rows)
            new_chat_history_rows = list()
            for row in chat_history_rows:
                row_list = list(row)
                row_username = userid_to_username_map[row[1]]
                row_list.append(row_username)
                new_chat_history_rows.append(row_list)

            list_of_python_dict = []
            for row in new_chat_history_rows:
                message_dict = {
                    'author': row[-1],
                    'content': row[3],
                    'timpestamp': str(row[2])
                }
                list_of_python_dict.append(message_dict)

        #
        # messages = Message.last_10_messages()

        # Data needed....
        # 'author': author,
        # 'content': messagecontext,
        # 'timestamp': str(row[0])

        content = {
            'command': 'messages',
            # 'messages': self.messages_to_json(messages),
            # A list of python dictionaries
            'messages': list_of_python_dict
        }
        print(content, "FJFDPIOJPFDOIWEOPFIJFW")
        self.send_chat_message(content)

    def new_message(self, data):
        # Create and save the message
        print('new message created: ', data)
        author = data['from']
        user_id = data['user_id']
        chatroom_id = data["chatroomid"]
        messagecontext = data['message']

        with connection.cursor() as cursor:
            create_new_message_query = """
                INSERT INTO PrivateChatHistory (chatroomid, senderid, messagecontext) 
                VALUES (%s, %s, %s);
            """
            cursor.execute(create_new_message_query, [chatroom_id, user_id, messagecontext])

            retrieve_created_time_history_query = """
                SELECT messagetime FROM PrivateChatHistory
                WHERE chatroomid = %s AND senderid = %s AND messagecontext = %s;
            """
            cursor.execute(retrieve_created_time_history_query, [chatroom_id, user_id, messagecontext])
            row = cursor.fetchone()


        # author_user = User.objects.filter(username=author)[0]
        # message = Message.objects.create(
        #     author=author_user, content=data['message']
        # )
        content = {
            'command': 'new_message',
            # 'message': self.message_to_json(message)
            'message': {
                'author': author,
                'content': messagecontext,
                'timestamp': str(row[0])
            }
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
