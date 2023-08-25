from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Token(models.Model):
     full_name = models.CharField(max_length=50)    
     user = models.ForeignKey(User,default=None, on_delete=models.CASCADE)
