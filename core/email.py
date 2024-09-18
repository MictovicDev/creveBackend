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

def send_talent_booking_mail(talentname, clientname, talentemail):
    try:
        subject = 'You have a job Offer'
        talentname = talentname.capitalize()
        email_data = {
            'talentname': talentname,
            'clientname' : clientname
        }
        html_message = render_to_string('core/request.html',email_data)
        from_email = os.environ.get('EMAIL_USER')
        recipient_list = [talentemail]
        send_mail(subject,
            message=None,
            from_email=from_email,
            recipient_list= recipient_list,
            fail_silently=False,
            html_message=html_message)
        return talentname
    except Exception as e:
        logger.error(f"Email sending failed: {str(e)}")

def send_client_booking_mail(clientname, talentname, clientemail):
    try:
        subject = 'Your Request has been made'
        clientname = clientname.capitalize()
        email_data = {
            'clientname': clientname,
            'talentname' : talentname
        }
        html_message = render_to_string('core/clientrequest.html',email_data)
        from_email = os.environ.get('EMAIL_USER')
        recipient_list = [clientemail]
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