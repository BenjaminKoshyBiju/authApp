from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import RegistrationForm, TokenForm
from .models import Token, LoginUser,register
from .tasks import generate_and_send_code


def Register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_verified = False
            user.save()
            generate_and_send_code(user.email,user.username)
           
            print('token created no pass though')
            

            # Send verification email asynchronously using Celery
  
            messages.success(request, 'Registration successful! Check your email for verification.')
            return redirect('token',user_id=user.id)
    else:
        form = RegistrationForm()
    return render(request, 'registration.html', {'form': form})


# def verify_token(request):
#     if request.method == 'POST':
#         token_form = TokenForm(request.POST)
#         if token_form.is_valid():
#             token_code = token_form.cleaned_data['code']
#             user = request.user
#             print(user)
#             try:
#                 token = Token.objects.get(user=user, code=token_code)
#                 token.delete()
#                 print('Try block working')
#                 # Mark the user's email as verified
#                 user.is_verified = True
#                 user.save()

#                 # Create a LoginUser instance and copy data
#                 login_user = LoginUser.objects.create(user=user)
#                 login_user.save()

#                 messages.success(request, 'Account verified! You can now log in.')
#                 return redirect('login')
#             except Token.DoesNotExist:
#                 print('Except block working')
#                 messages.error(request, 'Invalid or expired verification code.')
#     else:
#         token_form = TokenForm()
#     return render(request, 'token.html', {'token_form': token_form})


def verify_token(request, user_id):
    try:
        user = register.objects.get(pk=user_id)
    except register.DoesNotExist:
        messages.error(request, 'User not found with the provided ID.')
        return redirect('login')  # Redirect to an appropriate page

    if request.method == 'POST':
        token_form = TokenForm(request.POST)
        if token_form.is_valid():
            token_code = token_form.cleaned_data['code']
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
    return render(request, 'token.html', {'token_form': token_form})

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


def dashboard(request):
   

    return render(request, 'dashboard.html')
     
