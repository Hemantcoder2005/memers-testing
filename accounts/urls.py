from django.urls import path,include
from . import views
urlpatterns = [
    path('login/',views.handlelogin,name='login'),
    path('signup',views.signup,name='signup'),
    path('forgotpassword',views.forgot_password,name='forgot_password'),
    path('logout',views.handlelogout,name='logout'),
    
]
