from django.core.mail import send_mail
from app.utils.constant import *
from django.conf import settings
import datetime as dt


def notify_admin():
    print "send mail"
    send_mail('Category changed ', "Hello", 'shubhamdrolia87@gmail.com', settings.LIST_FOR_MAILS, fail_silently=False)


