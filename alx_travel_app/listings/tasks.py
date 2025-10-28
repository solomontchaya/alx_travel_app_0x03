from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_booking_confirmation_email(user_email, booking_id):
    subject = f'Booking Confirmation #{booking_id}'
    message = (
        f'Thank you for your booking! '
        f'Your booking with ID {booking_id} has been successfully created.'
    )
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list)
    return f"Confirmation email sent to {user_email} for booking {booking_id}"
