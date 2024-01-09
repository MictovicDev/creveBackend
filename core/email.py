from django.core.mail import send_mail
from django.template.loader import render_to_string
import os
# from celery import shared_task
import logging

logger = logging.getLogger(__name__)

# @shared_task
def send_linkmail(first_name,useremail,token):
    try:
        token = str(token)
        tokencheck = token
        url = f"http://bildingapi.onrender.com/auth/activation/{tokencheck}"
        subject = 'Welcome to Bilding Construction'
        name = first_name.capitalize()
        email_data = {
            'url': url,
            'token': tokencheck,
            'name': name
        }
        html_message = render_to_string('authentication/email.html',email_data)
        from_email = os.environ.get('EMAIL_USER')
        recipient_list = [useremail]
        send_mail(subject,
            message=None,
            from_email=from_email,
            recipient_list= recipient_list,
            fail_silently=False,
            html_message=html_message)
        print('sent')
        return name
    except Exception as e:
        logger.error(f"Email sending failed: {str(e)}")