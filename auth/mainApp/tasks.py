from celery import shared_task
from django.core.mail import send_mail
import random
import string
from .models import register, Token

def generate_random_code():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))

@shared_task
def generate_and_send_code(email):
    user = register.objects.get(email=email)
    
    try:
        existing_code = Token.objects.get(user=user)
        code = existing_code.code
    except Token.DoesNotExist:
        code = generate_random_code()
        Token.objects.create(user=user, code=code)
        print("Saved Code in Token:", code) 
    send_verification_email.delay(email, code)




@shared_task
def send_verification_email(email, code):
    print("Sending email with code:", code)
    subject = 'Your Verification Code'
    message = f'the code is {code}'
    from_email = 'benjaminkoshy038@gmail.com'
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)








