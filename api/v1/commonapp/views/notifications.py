import logging
from celery.task import task
from twilio.rest import Client
from v1.commonapp.views.logger import logger
from django.core.mail import EmailMultiAlternatives
from v1.commonapp.views.secret_reader import SecretReader
from v1.utility.models import utility_master
import html
from bs4 import BeautifulSoup
from django.core.mail import send_mail
from django.core.mail.backends.smtp import EmailBackend

# Local logging
local_logger = logging.getLogger('django')
secret_reader = SecretReader()


@task(name='send_mail')
def send_email(subject, from_email, to, body=None, attachments=None, html=None):
    try:
        backend = EmailBackend(host='smtp.sendgrid.net', port=587,
                               username='apikey', use_tls=True, fail_silently=False)
        msg = EmailMultiAlternatives(subject=subject, body=body, from_email=from_email, to=to, connection=backend,
                                     attachments=attachments)
        if html is not None:
            msg.attach_alternative(html, "text/html")
        msg.send(fail_silently=False)
    except Exception as e:
        local_logger.info("In send mail " + str(e))
        logger().log(e, 'LOW')


@task(name='send_sms')
def send_sms(sms_body, from_number, to_number):
    try:
        account_sid = secret_reader.get_twilio_sid()
        auth_token = secret_reader.get_twilio_token()
        client = Client(account_sid, auth_token)
        print(account_sid, auth_token)
        message = client.messages.create(
            body=sms_body,
            from_=from_number,
            to=to_number
        )
        print(message.sid)
    except Exception as e:
        logger().log(e, 'LOW', message=str(e))


def handle_communications(type, instance):
    array_of_variables = {}
    if type == 'Utility':
        utility = utility_master.get_utility_by_id(instance.id)
        array_of_variables = {
            "{Utility.email}": utility.email_id,
            "{Utility.utility_name}": utility.name,

        }
    return array_of_variables


def html_handler(html_template, array):
    # Replace the Keys with their actual values
    for k, v in array.items():
        html_template = html_template.replace(k, array[k])
    return html_template
