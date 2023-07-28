from django.urls import path
from . import views
#urls are here
urlpatterns = [
    path('upload',views.upload,name="upload"),
]
