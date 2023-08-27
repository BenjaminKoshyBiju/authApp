from django import forms
from .models import register,Token
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    full_name = forms.CharField(max_length=150, required=True)

    class Meta:
        model = register
        fields = ['full_name','username','email',]
        exclude = ['is_verified']

     
class TokenForm(forms.ModelForm):
    class Meta:
        model = Token
        fields = ['code']

