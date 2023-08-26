from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
# Create your models here.



class register(AbstractUser):
    full_name = models.CharField(max_length=50)
    is_verified = models.BooleanField(default=False)

class Token(models.Model):
    code = models.CharField(max_length=50)
    user = models.ForeignKey(register, default=None, on_delete=models.CASCADE)


class LoginUser(models.Model):
    user = models.OneToOneField('mainApp.register', on_delete=models.CASCADE)
    
