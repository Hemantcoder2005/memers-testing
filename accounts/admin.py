from django.contrib import admin
from .models import CustomUser

class AdminUsers(admin.ModelAdmin):
    list_display=['username','email','first_name']

# Register your models here.
admin.site.register(CustomUser,AdminUsers)