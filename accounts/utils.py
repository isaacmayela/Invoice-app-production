import string
import random
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
import logging
import uuid

def generate_username (first_name):
    chars=string.ascii_uppercase + string.digits
    username = first_name + "".join(random.choices(chars, k=12))
    return username

logger = logging.getLogger(__name__)
def send_email_confirmation(subject:str, receivers: list, template:str, context:dict):
    """This function sends emails to specific users"""
    print("est dans la fonction")
    try:
        message = render_to_string(template, context)
        send_mail(
            subject,
            message,
            receivers,
            settings.EMAIL_HOST_USER,
            fail_silently=True,
            html_message=message
        )
        return True

    except Exception as e:
        logger.error(e)

    return False

def validate_email_token(valeur):
    try:
        uuid_obj = uuid.UUID(valeur, version=4)
        return str(uuid_obj) == valeur
    except ValueError:
        return False