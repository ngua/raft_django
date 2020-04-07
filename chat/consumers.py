import json
from uuid import UUID
from django.conf import settings
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatUser, Message, Room, StaffChatProfile


CHAT_MESSAGE_LIMIT = getattr(settings, 'CHAT_MESSAGE_LIMIT', 20)


def display_time(time):
    return time.strftime('%H:%M')


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
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
        messages = await self.get_messages()
        response = {
            'command': 'messages',
            'messages': messages
        }
        await self.send(json.dumps(response))

    async def receive(self, text_data):
        commands = {
            'list-messages': self.list_messages,
            'new-message': self.new_message
        }
        json_data = json.loads(text_data)
        command = json_data['command']
        await commands.get(command)(json_data)

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))

    async def get_uid(self, uid):
        try:
            uid = UUID(uid, version=4)
            return uid
        except ValueError as e:
            raise e

    @database_sync_to_async
    def get_room(self, uid):
        self.room, _ = Room.objects.get_or_create(room_id=uid)
        if self.user not in self.room.chat_users.all():
            self.room.chat_users.add(self.user)

    @database_sync_to_async
    def get_author(self, message):
        return str(message.author.uid)

    @database_sync_to_async
    def create_message(self, author, text):
        message = Message.objects.create(
            author=author,
            text=text
        )
        self.room.messages.add(message)
        self.room.save()
        return message

    @database_sync_to_async
    def get_messages(self):
        messages = self.room.messages.order_by('-time_stamp').all()[:CHAT_MESSAGE_LIMIT]
        return [
            {
                'text': message.text,
                'author': str(message.author.uid),
                'time': display_time(message.time_stamp)
            } for message in messages
        ]

    async def new_message(self, text):
        message = await self.create_message(
            author=self.user,
            text=text
        )
        response = {
            'command': 'new-message',
            'message': {
                'text': message.text,
                'author': await self.get_author(message),
                'time': display_time(message.time_stamp)
            }
        }
        await self.channel_layer.group_send(
            self.room_group_name, {
                'type': 'chat_message',
                'message': response
            }
        )


class CustomerChatConsumer(ChatConsumer):
    async def connect(self):
        session_uid = await self.get_session_uid()
        uid = await self.get_uid(self.scope['url_route']['kwargs']['uid'])
        self.room_name = f'{uid}'
        self.room_group_name = f'chat_{self.room_name}'
        if str(uid) != session_uid:
            await self.disconnect(403)
        else:
            self.user, _ = await self.get_chat_user(uid)
            await self.get_room(uid)
            await super().connect()

    async def new_message(self, data):
        text = data['text']
        await super().new_message(text)

    @database_sync_to_async
    def get_session_uid(self):
        return self.scope['session']['chat_uid']

    @database_sync_to_async
    def get_chat_user(self, uid):
        return ChatUser.objects.get_or_create(uid=uid)


class AdminChatConsumer(ChatConsumer):
    async def connect(self):
        uid = await self.get_uid(self.scope['url_route']['kwargs']['uid'])
        user = self.scope['user']
        self.room_name = uid
        self.room_group_name = f'chat_{self.room_name}'
        if not user.is_authenticated or not user.is_staff:
            await self.disconnect(403)
        else:
            self.user = await self.get_staff_chat_profile(user.username)
            await self.get_room(uid)
            await super().connect()

    async def new_message(self, data):
        text = data['text']
        await super().new_message(text)

    @database_sync_to_async
    def get_staff_chat_profile(self, username):
        return StaffChatProfile.objects.get(user__username=username)
