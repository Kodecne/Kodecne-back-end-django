# Generated by Django 5.1.7 on 2025-05-23 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_chatmessage_image_alter_chatmessage_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatmessage',
            name='image',
        ),
        migrations.AddField(
            model_name='chatmessage',
            name='images',
            field=models.JSONField(blank=True, default=list),
        ),
    ]
