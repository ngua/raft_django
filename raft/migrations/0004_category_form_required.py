# Generated by Django 3.0.4 on 2020-03-18 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('raft', '0003_auto_20200315_2022'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='form_required',
            field=models.BooleanField(default=True),
        ),
    ]
