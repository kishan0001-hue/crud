from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_otp_email(username, email, otp):
    send_mail(
        subject="Email Verification OTP",
        message=f"""
Hello {username},

Your OTP is: {otp}

This OTP will expire in 5 minutes.

Please do not share this OTP with anyone.
""",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )

    return "OTP email sent successfully"