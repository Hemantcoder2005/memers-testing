from django.urls import path
from .views import home
#urls are here
urlpatterns = [
    path('',home,name="home"),
]
