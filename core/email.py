from django.core.mail import send_mail
from django.template.loader import render_to_string
import os
# from celery import shared_task
import logging

logger = logging.getLogger(__name__)


# @shared_task
def send_linkmail(fullname,useremail,otp):
    try:
        subject = 'Welcome to Creve'
        name = fullname.capitalize()
        email_data = {
            'otp': otp,
            'name': name
        }
        print(email_data)
        html_message = render_to_string('core/email.html',email_data)
        from_email = os.environ.get('EMAIL_USER')
        recipient_list = [useremail]
        send_mail(subject,
            message=None,
            from_email=from_email,
            recipient_list= recipient_list,
            fail_silently=False,
            html_message=html_message)
        return name
    except Exception as e:
        logger.error(f"Email sending failed: {str(e)}")
    return 'Sent'

def send_booking_mail(fullname, clientname, useremail):
    try:
        subject = 'You have a job Offer'
        name = fullname.capitalize()
        email_data = {
            'name': name,
            'client' : clientname
        }
        html_message = render_to_string('core/request.html',email_data)
        from_email = os.environ.get('EMAIL_USER')
        recipient_list = [useremail]
        send_mail(subject,
            message=None,
            from_email=from_email,
            recipient_list= recipient_list,
            fail_silently=False,
            html_message=html_message)
        return name
    except Exception as e:
        logger.error(f"Email sending failed: {str(e)}")

def message_sent_mail(fullname, clientname, useremail, message):
    try:
        subject = 'One New Message'
        name = fullname.capitalize()
        email_data = {
            'name': name,
            'client' : clientname,
            'message': message
        }
        html_message = render_to_string('core/message.html',email_data)
        from_email = os.environ.get('EMAIL_USER')
        recipient_list = [useremail]
        send_mail(subject,
            message=None,
            from_email=from_email,
            recipient_list= recipient_list,
            fail_silently=False,
            html_message=html_message)
        return name
    except Exception as e:
        logger.error(f"Email sending failed: {str(e)}")