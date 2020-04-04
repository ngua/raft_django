from uuid import uuid4
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Room(models.Model):
    room_id = models.UUIDField(null=False, editable=False, default=uuid4)
    last_active = models.TimeField(auto_now=True)
    chat_users = models.ManyToManyField('ChatUser')

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.room_id}')"

    def __str__(self):
        chat_users = ','.join([
            str(chat_user.uid) for chat_user in self.chat_users.all()
        ])
        return f"{self.room_id}: {chat_users}"


class Message(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    text = models.TextField()
    time_stamp = models.TimeField(auto_now_add=True)

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.content_object}', '{self.text}')"

    def __str__(self):
        return f"{self.content_object}@{self.time_stamp}: {self.text}"


class ChatUser(models.Model):
    uid = models.UUIDField(null=False, editable=False, default=uuid4)
    messages = GenericRelation(Message, related_query_name='author')

    def __repr__(self):
        return f"{self.__class__.__name__}('{str(self.uid)}')"

    def __str__(self):
        return str(self.uid)
