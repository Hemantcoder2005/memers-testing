from django.core.mail import send_mail
from django.conf import settings
def send_email_to_client(client_mail=None,message=None):
    subject="OTP verification"
    message
    from_email=settings.EMAIL_HOST_USER
    recipient_list=[client_mail]
    return send_mail(subject, message,from_email,recipient_list)