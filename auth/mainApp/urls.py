from .import views
from django.urls import path
urlpatterns = [
     path('',views.register,name='Register'),
     path('token',views.verify_token,name='token'),
     path('login',views.user_login,name='login'),
]