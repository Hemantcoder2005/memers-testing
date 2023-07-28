from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager

# Create your models here.
class CustomUser(AbstractUser):
    username=models.CharField(max_length=50,unique=True,default='')
    profile_img=models.ImageField(upload_to='profile_img/',null=True,blank=True,default='profile_img/default-user.jpg')
    email=models.EmailField(unique=True,default='')
    authenticate_email=models.BooleanField(default=False)
    otp=models.CharField(max_length=200,null=True,blank=True)
    otp_date=models.DateTimeField(blank=True,null=True)
    dob=models.DateField(blank=True,null=True)
    def __str__(self):
        return self.username
    objects=UserManager()
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]
    