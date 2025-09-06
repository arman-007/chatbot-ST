from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings


def send_verification_email(user_id):
    """
    Sends a verification email to a newly registered user.
    """
    try:
        user = User.objects.get(pk=user_id)
        subject = 'Welcome to Your AI Chatbot!'
        message = f'Hi {user.username},\n\nThank you for registering. We are excited to have you on board.'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user.email]

        send_mail(subject, message, from_email, recipient_list)
        
        print(f"Successfully sent verification email to {user.email}")
    except User.DoesNotExist:
        print(f"User with id {user_id} does not exist.")
    except Exception as e:
        print(f"Failed to send email to user_id {user_id}: {e}")