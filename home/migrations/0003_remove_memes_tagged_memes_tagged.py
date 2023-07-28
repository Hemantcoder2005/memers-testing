# Generated by Django 4.0.6 on 2023-07-22 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_tags_memes_tagged'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='memes',
            name='tagged',
        ),
        migrations.AddField(
            model_name='memes',
            name='tagged',
            field=models.ManyToManyField(to='home.tags'),
        ),
    ]
