from django.apps import AppConfig
from home import models
from django import forms
memes=models.memes

class CreatorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'creator'
class CreateMemes(forms.ModelForm):
    class Meta:
        model=memes
        fields=['title','meme','tagged']