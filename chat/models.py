from uuid import uuid4
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class ChatClient(models.Model):
    uid = models.UUIDField(null=False, editable=False, default=uuid4)


class Room(models.Model):
    room_id = models.UUIDField(null=False, editable=False, default=uuid4)
    last_active = models.DateTimeField(auto_now=True)
    chat_users = models.ManyToManyField(ChatClient)

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.room_id}')"

    def __str__(self):
        return f"{self.room_id}: {self.last_active}"


class Message(models.Model):
    author = models.ForeignKey(ChatClient, on_delete=models.CASCADE)
    text = models.TextField()
    time_stamp = models.TimeField(auto_now_add=True)

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.author}', '{self.text}')"

    def __str__(self):
        return f"{self.author}@{self.time_stamp}: {self.text}"


class ChatUser(ChatClient):
    def __repr__(self):
        return f"{self.__class__.__name__}('{str(self.uid)}')"

    def __str__(self):
        return str(self.uid)


class StaffChatProfile(ChatClient):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.user}')"

    def __str__(self):
        return f'{self.user.username}'


@receiver(post_save, sender=User)
def create_chat_profile(sender, created, instance, **kwargs):
    if created:
        StaffChatProfile.objects.create(user=instance)


@receiver
def save_chat_profile(sender, instance, **kwargs):
    instance.profile.save()
