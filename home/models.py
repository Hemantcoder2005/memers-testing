from django.db import models
from memers import settings
# from datetime import date
import django.utils.timezone

#variable
user=settings.AUTH_USER_MODEL

# Create your models here.
class Tags(models.Model):
    
    name=models.CharField(max_length=20)
    created_by=models.ForeignKey(user,on_delete=models.CASCADE,default=user)
    created_on=models.DateField(default=django.utils.timezone.now)
    meme_tagged=models.BigIntegerField(default=0)
    def __str__(self):
        return self.name

    
    

class memes(models.Model):
    title=models.CharField(max_length=200)
    author=models.ForeignKey(user,on_delete=models.CASCADE,default=user)
    meme=models.ImageField(upload_to='memes')
    tagged=models.ManyToManyField(Tags)
    created_on=models.DateField(default=django.utils.timezone.now)
    liked=models.ManyToManyField(user,default=None,blank=True,related_name='liked_memes')
    comments=models.CharField(max_length=100000000,null=True,blank=True)

   