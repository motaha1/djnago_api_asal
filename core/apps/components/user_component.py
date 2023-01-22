from logging import getLogger
from django.db import IntegrityError
from rest_framework.exceptions import NotFound, ValidationError, PermissionDenied
from core.apps.components.firebase import  firebase_chat, firebase_how_iam_talk, firebase_login, firebase_sendNotification, signup_firebase

from core.apps.users.constants import InternalCustomAdminActions
from core.apps.components.emails import send_otp_via_email
from core.apps.users.models import PatientProfile, User, SpecialistProfile, UserMedia
import requests
import pyodbc 


logger = getLogger(__name__)


class UserComponent:
    @staticmethod
    def change_user_password(user, new_password):
        # Auth0Service().change_auth0_user_password(user=user, new_password=new_password)
        user.set_password(new_password)
        user.save()

    @staticmethod
    def update_patient_profile(user, user_info):
        # Auth0Service().change_auth0_user_userinfo(user=user, info=user_info, source_endpoint=SourceEndpoint.FE)
        user.username = user_info.get('username')
        user.save(update_fields=['username'])

    # @staticmethod
    # def verify_user_email(email: str, identity: any):
    #     return Auth0Service().verify_user_email(email, identity)

    @staticmethod
    def create_new_patient(email: str, username: str, mobile: str, password: any,
                           gender: str, city: str, birthdate: any):
        try:
            new_user = User(email=email,
                            password=password,
                            username=username,
                            mobile=mobile,
                            gender=gender,
                            city=city,
                            birthdate=birthdate,
                            is_patient=True)

            new_user._raw_password = password
            new_user.action = InternalCustomAdminActions.REGISTERED_USER

            new_user.save()

            new_patient = PatientProfile(user=new_user)
            new_patient.save()
            otp = send_otp_via_email(email)
            new_patient.otp = otp
            signup_firebase(id = new_patient.id , email = email , password = password ,name=username ,avatar='https://d2pas86kykpvmq.cloudfront.net/images/humans-3.0/ava-1.png' , type='patient' )
            new_patient.save()



            return new_user
        except IntegrityError:
            raise ValidationError("email already used")
        except ValidationError:
            raise ValidationError("invalid email")
        except ValueError:
            raise ValidationError("invalid email or password")

    @staticmethod
    def create_new_specialist(email: str, username: str, mobile: str, password: any):
        try:
            new_user = User(email=email,
                            password=password,
                            username=username,
                            mobile=mobile,
                            is_specialist=True,
                            is_active=False)

            new_user._raw_password = password
            new_user.action = InternalCustomAdminActions.REGISTERED_USER

            new_user.save()

            new_patient = SpecialistProfile(user=new_user)
            new_patient.save()
            signup_firebase(id = new_patient.id , email = email , password = password ,name=username ,avatar='https://d2pas86kykpvmq.cloudfront.net/images/humans-3.0/ava-1.png' , type='Special' )

            return new_user
        except IntegrityError:
            raise ValidationError("email already used")
        except ValidationError:
            raise ValidationError("invalid email")
        except ValueError:
            raise ValidationError("invalid email or password")


    @staticmethod
    def update_user_avatar(user_id: any, image: any):
        user_avatar = UserMedia.objects.create(profile_img=image)
        user = User.objects.get(pk=user_id)
        user.avatar = user_avatar
        user.save()
        return user_avatar


    @staticmethod
    def login(email , password) : 

        user_info = firebase_login(email = email , password = password)
        
        if user_info is not None :
            user_id = user_info['id']
            
            if user_info['type']  == 'patient':
                user =  requests.get (f'http://127.0.0.1:8000/api/users/patients/{user_id}').json()
                

                return(user)
            
            elif user_info['type']  == 'Special':
                user = requests.get (f'http://127.0.0.1:8000/api/users/specialists/{user_id}').json()
                return(user)
                

        
        else :
            return ('email or password worng')


    @staticmethod
    def chat(sender , receiver , text , time) :
        firebase_chat(sender=sender , receiver=receiver , text=text , time= time)
        

    @staticmethod
    def palestineid(name , ID):
        

# msa = [x for x in pyodbc.drivers() if'ACCESS' in x.upper()]
# print(f'hello ----- {msa}')

        try :
            constr = 'Driver={Microsoft Access Driver (*.mdb, *.accdb)};Dbq=' + 'D:\sejel\sejel.mdb'
            con = pyodbc.connect(constr)
            print('ok')
            cur = con.cursor()

            cur.execute(f"SELECT * FROM Sgaza where id = '{ID}'")
            for x in cur.fetchall():
                pass 
            cur.close()

            if(x[1]==name):
                return x[1]+" "+x[2]+" "+x[3]+" "+x[4]
            
            else :
                return 'error data'





        except pyodbc.Error as e :
            print(e)


    
    @staticmethod
    def sendNotification(title , msg , token):
        firebase_sendNotification(token=(token) , msg=msg , title=title)

    @staticmethod

    def how_iam_talk(email) :
       user =  firebase_how_iam_talk(email)
       return user

