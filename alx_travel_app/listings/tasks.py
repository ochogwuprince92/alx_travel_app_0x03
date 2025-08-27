from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_booking_email(user_email, booking_id):
    subject = 'Booking Confirmation'
    message = f'Your booking with ID {booking_id} has been confirmed.'
    
    send_mail(  
                subject, 
                message, 
                settings.DEFAULT_FROM_EMAIL,  # Use the default from email defined in settings
                [user_email], # Send to the user's email address
                fail_silently=False,
    )