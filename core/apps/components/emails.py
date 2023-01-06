from django.core.mail import send_mail
import random
from django.conf import settings
from ..users.models import *

def send_otp_via_email(email):
    subject = 'veridication'
    otp = random.randint(100000 ,999999)
    message = f'your otp is {otp}'
    email_from = settings.EMAIL_HOST
    send_mail(subject , message , email_from , [email])
    return otp




def send_doc_doctor(email , pk):
    subject = 'send doc'
    
    #otp = random.randint(1000 ,9999)
    message = f'go there http://127.0.0.1:8000/api/Doctordocumint/{pk}/'
    email_from = settings.EMAIL_HOST
    send_mail(subject , message , email_from , [email])
    # user_obj = Nurse.objects.get(email=email)
    # user_obj.otp = otp 
    # user_obj.save()