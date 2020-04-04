import json
from uuid import UUID
from django.conf import settings
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatUser, Message, Room


CHAT_MESSAGE_LIMIT = getattr(settings, 'CHAT_MESSAGE_LIMIT', 20)


def display_time(date):
    return date.strftime('%H:%m')


class ChatConsumer(AsyncWebsocketConsumer):
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def list_messages(self, data):
        messages = await self.get_messages(self.room_name)
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
        except ValueError:
            pass

    @database_sync_to_async
    def get_room(self, uid):
        return Room.objects.get_or_create(room_id=uid)

    @database_sync_to_async
    def get_author(self, message):
        return str(message.author.get().uid)

    @database_sync_to_async
    def create_message(self, author, text):
        return Message.objects.create(
            content_object=author,
            text=text
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
            chat_user, _ = await self.get_chat_user(uid)
            user_room, _ = await self.get_room(uid)
            await self.add_user(user_room, chat_user)

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()

    async def new_message(self, data):
        uid, text = data['from'], data['text']
        chat_user, _ = await self.get_chat_user(uid)
        message = await self.create_message(
            author=chat_user,
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

    @database_sync_to_async
    def get_session_uid(self):
        return self.scope['session']['chat_uid']

    @database_sync_to_async
    def add_user(self, room, chat_user):
        if chat_user not in room.chat_users.all():
            room.chat_users.add(chat_user)

    @database_sync_to_async
    def get_chat_user(self, uid):
        return ChatUser.objects.get_or_create(uid=uid)

    @database_sync_to_async
    def get_messages(self, room_id):
        room = Room.objects.get(room_id=room_id)
        messages = Message.objects.filter(
            author__in=room.chat_users.all()
        ).order_by('-time_stamp').all()[:CHAT_MESSAGE_LIMIT]
        return [
            {
                'text': message.text,
                'author': str(message.author.get().uid),
                'time': display_time(message.time_stamp)
            } for message in messages
        ]


class AdminChatConsumer(ChatConsumer):
    async def connect(self):
        uid = await self.get_uid(self.scope['url_route']['kwargs']['uid'])
        room, _ = await self.get_room(uid)
        self.room_name = f'{uid}'
        self.room_group_name = f'chat_{self.room_name}'
        self.user = self.scope['user']
        if not self.user.is_authenticated or not self.user.is_staff:
            await self.disconnect(403)
        else:
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
