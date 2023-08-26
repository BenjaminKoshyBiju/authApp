from .import views
from django.urls import path
urlpatterns = [
     path('',views.register,name='Register'),
     path('token',views.token,name='token'),
     path('login',views.token,name='login'),
]