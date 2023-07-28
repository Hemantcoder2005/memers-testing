# Generated by Django 4.0.6 on 2023-07-25 11:03

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0009_memes_comments_memes_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='memes',
            name='likes',
        ),
        migrations.AddField(
            model_name='memes',
            name='liked',
            field=models.ManyToManyField(blank=True, default=None, related_name='users_liked', to=settings.AUTH_USER_MODEL),
        ),
    ]
