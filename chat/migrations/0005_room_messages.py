# Generated by Django 3.0.4 on 2020-04-07 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_room_last_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='messages',
            field=models.ManyToManyField(to='chat.Message'),
        ),
    ]