from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings


# Getting the user role function 
def detectUser(user):
    if user.role == 1:
        redirectUrl = 'vendorDashboard'
        return redirectUrl
    elif user.role == 2:
        redirectUrl = 'custDashboard'
        return redirectUrl
    elif user.role == None and user.is_superadmin:
        redirectUrl = '/admin'
        return redirectUrl


# Email verification function
def send_verification_email(request, user, mail_subject, email_template):
    from_email = settings.DEFAULT_FROM_EMAIL
    # First of all, we need to get the current site, domain
    current_site = get_current_site(request)
    # Message_body
    message = render_to_string(email_template,{
        'user': user,
        'domain': current_site,
        # We can not send user.pk, we need to encode it
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_email = user.email
    # Package that we are using for sending the email
    mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
    mail.send()


def send_notification(mail_subject, mail_template, context):
    from_email = settings.DEFAULT_FROM_EMAIL
    message = render_to_string(mail_template, context)
    # We check if 'to_email' is string type. If not, we add it to_list, as it is needed for 'to' parameter while sending email.
    if(isinstance(context['to_email'], str)):
        to_email = []
        to_email.append(context['to_email'])
    else:
        to_email = context['to_email']
    # To param is waiting for string type
    mail = EmailMessage(mail_subject, message, from_email, to=to_email)
    mail.send()