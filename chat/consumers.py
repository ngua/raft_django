import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatUser, Message


class CustomerChatConsumer(AsyncWebsocketConsumer):
    async def init_chat(self, data):
        uid = data['uid']
        chat_user, _ = await self.get_chat_user(uid)
        response = {
            'command': 'init_chat',
        }
        await self.send(json.dumps(response))

    async def connect(self):
        self.room_name = 'test'
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def list_messages(self, data):
        messages = await self.get_messages(10)
        response = {
            'command': 'messages',
            'messages': messages
        }
        await self.send(json.dumps(response))

    async def new_message(self, data):
        uid, text = data['from'], data['text']
        chat_user, _ = await self.get_chat_user(uid)
        message = await self.create_message(
            author=chat_user,
            text=text
        )
        response = {
            'command': 'new_message',
            'message': {
                'text': message.text,
                'author': await self.get_author(message),
                'time': message.time_stamp.isoformat()
            }
        }
        await self.channel_layer.group_send(
            self.room_group_name, {
                'type': 'chat_message',
                'message': response
            }
        )

    async def receive(self, text_data):
        commands = {
            'init_chat': self.init_chat,
            'list_messages': self.list_messages,
            'new_message': self.new_message
        }
        json_data = json.loads(text_data)
        command = json_data['command']
        await commands.get(command)(json_data)

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))

    @database_sync_to_async
    def get_author(self, message):
        return str(message.author.get().uid)

    @database_sync_to_async
    def get_chat_user(self, uid):
        return ChatUser.objects.get_or_create(uid=uid)

    @database_sync_to_async
    def get_messages(self, limit):
        messages = Message.objects.all().order_by('-time_stamp')[:limit]
        return [
            {
                'text': message.text,
                'author': str(message.author.get().uid),
                'time': message.time_stamp.isoformat()
            } for message in messages
        ]

    @database_sync_to_async
    def create_message(self, author, text):
        return Message.objects.create(
            content_object=author,
            text=text
        )


class AdminChatConsumer(AsyncWebsocketConsumer):
    pass
