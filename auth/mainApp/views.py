from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import RegistrationForm, TokenForm
from .models import Token, LoginUser
from .tasks import send_verification_email

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_verified = False
            user.save()

            token = Token.objects.create(user=user)

            # Send verification email asynchronously using Celery
            send_verification_email.delay(user.email, token.code)

            messages.success(request, 'Registration successful! Check your email for verification.')
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def verify_token(request):
    if request.method == 'POST':
        token_form = TokenForm(request.POST)
        if token_form.is_valid():
            token_code = token_form.cleaned_data['code']
            user = request.user

            try:
                token = Token.objects.get(user=user, code=token_code)
                token.delete()

                # Mark the user's email as verified
                user.is_verified = True
                user.save()

                # Create a LoginUser instance and copy data
                login_user = LoginUser.objects.create(user=user)
                login_user.save()

                messages.success(request, 'Account verified! You can now log in.')
                return redirect('login')
            except Token.DoesNotExist:
                messages.error(request, 'Invalid or expired verification code.')
    else:
        token_form = TokenForm()
    return render(request, 'verification/verify_token.html', {'token_form': token_form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_verified:
            login(request, user)
            return redirect('dashboard')  # Redirect to the dashboard or relevant page
        elif user is not None and not user.is_verified:
            messages.error(request, 'Account is not yet verified.')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')
     
