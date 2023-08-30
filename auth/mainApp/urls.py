from .import views
from django.urls import path
from django.contrib.auth import views as auth_views
urlpatterns = [
     path('',views.Register,name='Register'),
     path('token/<int:user_id>',views.verify_token,name='token'),
     path('login',views.user_login,name='login'),
     path('dashboard',views.dashboard,name='dashboard'),
     path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]