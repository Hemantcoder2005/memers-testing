from django.contrib import admin
from .models import memes,Tags

class AdminMemes(admin.ModelAdmin):
    list_display=['id','author','created_on']
class AdminTags(admin.ModelAdmin):
    list_display=['name','created_by','created_on']

# Register your models here.
admin.site.register(Tags,AdminTags)
admin.site.register(memes,AdminMemes)
