# Generated by Django 4.0.6 on 2023-07-22 15:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0005_memes_created_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memes',
            name='author',
            field=models.ForeignKey(default='accounts.CustomUser', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
