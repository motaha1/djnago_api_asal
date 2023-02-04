# Create your views here.
from django.urls import path
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from core.apps.components.user_component import UserComponent
from core.apps.mixins import ReadWriteSerializerMixin
from core.apps.users.constants import BloodType, MedicalType, SpecialistType, CollegesDegrees
from core.apps.users.models import SpecialistProfile, PatientProfile
from core.apps.users.serializers import UserAvatarSerializer, WriteSpecialistSerializer, \
    ReadUserMiniInfoSerializer, ReadSpecialistSerializer, ReadPatientSerializer, WritePatientSerializer , ReadRatting ,WriteAppointmentSerializer , ReadAppointmentSerializer , ReadCommentSerializer  ,\
        FavSerializer , NotificationSerializer

from core.apps.users.models import *
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F  



#from django_filters.rest_framework import DjnagoFilterBackend

# import django_filters
import django_filters.rest_framework






class ListBloodTypeAPIView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    pagination_class = None

    def list(self, request, *args, **kwargs):
        values = [choice[0] for choice in BloodType.choices]
        return Response({"values": values}, 200)


class ListMedicalTypeAPIView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    pagination_class = None

    def list(self, request, *args, **kwargs):
        values = [choice[0] for choice in MedicalType.choices]
        return Response({"values": values}, 200)


class ListSpecialistTypeAPIView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    pagination_class = None

    def list(self, request, *args, **kwargs):
        values = [choice[0] for choice in SpecialistType.choices]
        return Response({"values": values}, 200)


class ListCollegesDegreesAPIView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    pagination_class = None

    def list(self, request, *args, **kwargs):
        values = [choice[0] for choice in CollegesDegrees.choices]
        return Response({"values": values}, 200)


class HealthCheckAPI(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
    throttle_scope = 'health_check_api'

    def retrieve(self, request, *args, **kwargs):
        return Response({"response": "API is working successfully."}, 200)


class PatientCreateAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    throttle_scope = 'sign-up'
    serializer_class = ReadUserMiniInfoSerializer
    
    


    def post(self, request, *args, **kwargs):
        user_data = request.data

        return Response(self.serializer_class(
            UserComponent.create_new_patient(email=user_data.get('email'),
                                             username=user_data.get('username'),
                                             mobile=user_data.get('mobile'),
                                             password=user_data.get('password'),
                                             gender=user_data.get('gender'),
                                             city=user_data.get('city'),
                                             birthdate=user_data.get('birthdate'))
            , many=False).data)


class SpecialistCreateAPIView(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)
    throttle_scope = 'sign-up'
    serializer_class = ReadUserMiniInfoSerializer



    def post(self, request, *args, **kwargs):
        user_data = request.data

        return Response(self.serializer_class(
            UserComponent.create_new_specialist(email=user_data.get('email'),
                                                username=user_data.get('username'),
                                                mobile=user_data.get('mobile'),
                                                password=user_data.get('password'))
            , many=False).data)


class UpdateUserAvatarView(generics.UpdateAPIView):
    permission_classes = (AllowAny,)
    throttle_scope = 'upload-user-avatar'
    serializer_class = UserAvatarSerializer

    def update(self, request, *args, **kwargs):
        return Response(self.serializer_class(
            UserComponent.update_user_avatar(user_id=self.kwargs.get('user_id'),
                                             image=request.data['avatar'])
            , many=False).data)


class RetrieveOrUpdateSpecialistAPIView(ReadWriteSerializerMixin,
                                        generics.RetrieveUpdateAPIView):
    read_serializer_class = ReadSpecialistSerializer
    write_serializer_class = WriteSpecialistSerializer
    permission_classes = (AllowAny,)
    

    def get_object(self):
        return SpecialistProfile.objects.get(pk=self.kwargs.get('specialist_id'))


class RetrieveOrUpdatePatientAPIView(ReadWriteSerializerMixin,
                                     generics.RetrieveUpdateAPIView):
    read_serializer_class = ReadPatientSerializer
    write_serializer_class = WritePatientSerializer
    permission_classes = (AllowAny,)

    def get_object(self):
        return PatientProfile.objects.get(pk=self.kwargs.get('patient_id'))

from rest_framework.filters import SearchFilter
from rest_framework.filters import OrderingFilter



############new#############
class AllSpecialList(generics.ListAPIView):
    
    serializer_class = ReadSpecialistSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend , SearchFilter , OrderingFilter]
    #filter_fields =('type')
    filterset_fields = ['type' , 'user__email' , 'at_home' , 'medical_type' , 'user__city'] #go to home or not 
    search_fields = ['user__username']
    ordering_fields = ['user__username', 'user__email']
    ordering = ['user__username']

    def get_queryset(self):
        return SpecialistProfile.objects.prefetch_related('rates').annotate(avg_rating=Avg('rates__stars')).order_by(F('-avg_rating').desc(nulls_last=True)).all()

class AllPatient(generics.ListAPIView):
    queryset = PatientProfile.objects.all()
    serializer_class = ReadPatientSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend , SearchFilter , OrderingFilter]
    #filter_fields =('type')
    filterset_fields = ['user__email'] #go to home or not 
    search_fields = ['user__username']
    ordering_fields = ['user__username', 'user__email']
    ordering = ['user__username']

class RattingView(generics.CreateAPIView) :

    queryset = Ratting.objects.all()
    serializer_class = ReadRatting
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend , SearchFilter , OrderingFilter]
    filterset_fields = ['specialist__user__username'  ,'patient__user__username' ]



class AppointmentWrite (generics.CreateAPIView):

     serializer_class = WriteAppointmentSerializer
     queryset = Appointment.objects.all()
     ##### new 
     
        

class Appointmentview (generics.ListAPIView):

     serializer_class = ReadAppointmentSerializer
     queryset = Appointment.objects.all().exclude(status = 'cancelled' )
     filter_backends = [django_filters.rest_framework.DjangoFilterBackend , SearchFilter , OrderingFilter]
     filterset_fields = ['specialist__id',  'specialist__user__username','specialist__user__email','patient__user__username' , 'date', 'patient__user__email' ,'patient__id' ,'status' ]

     

############# otp verify #######
class Otpverify(generics.CreateAPIView) : 
    serializer_class = ReadPatientSerializer
    
    def post(self, request, *args, **kwargs):
        data = request.data
        try : 
            patient = PatientProfile.objects.get(user__email =data['email'])
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
  

        if patient.otp == data['otp']:
                patient.user.is_active = True
                patient.user.save()


                return Response(self.serializer_class(patient , many = False).data)
            
        else :
            return Response(status=status.HTTP_403_FORBIDDEN)




    
class login (generics.CreateAPIView):

    def post(self, request, *args, **kwargs):
        email = request.data['email']
        password = request.data['password']

        user = UserComponent.login(email = email , password = password)
        print('hello')
        return Response(user)



class chat (generics.CreateAPIView):

    def post (self, request, *args, **kwargs):
        sender = request.data['sender']
        receiver = request.data['receiver']
        time = request.data['time']
        text = request.data['text']
        # flag= 0

        # try :
            
        #     token = SpecialistProfile.objects.get(user__email = receiver).fcm_token
        
        # except :
        #     token = PatientProfile.objects.get(user__email = receiver).fcm_token
        #     flag = 1 
        
        # if(flag==1) :
        #     name = 

        receiver_token = User.objects.get(email=receiver).fcm_token
        sender_name = User.objects.get(email= sender ).username
        receiver_id = User.objects.get(email=receiver)


        
        if(receiver_token ==None):
            receiver_token = 'nothing'

        print(receiver_token)
        print(sender_name)


        UserComponent.chat(sender=sender , receiver=receiver , time=time , text=text)
        UserComponent.sendNotification(token= receiver_token,title= f'new massage from {sender_name}' , msg=text)
        
        notify = Notification(title = text , msg =f'new massage from {sender_name}' ,user =  receiver_id )
        notify.save()

        return Response('its sent !')

class palestineId (generics.CreateAPIView):

    def post (self, request, *args, **kwargs):
        name = request.data['name']
        id = request.data['id']
        res = UserComponent.palestineid(name=name , ID=id)
        return Response(res)




class sendNotification(generics.CreateAPIView):
    def post (self, request, *args, **kwargs) :
        token = request.data['token']
        msg = request.data['msg']
        tiltle = request.data['title']
        try:
            UserComponent.sendNotification(msg=msg, title=tiltle, token=token)
            return Response('ok')
        except :
            return Response('error')


class Comments (generics.ListCreateAPIView):
    serializer_class = ReadCommentSerializer
    queryset = Comment.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend , SearchFilter , OrderingFilter]

    filterset_fields = ['created_at'] #go to home or not 
    search_fields = ['user__username']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def post (self, request, *args, **kwargs) : 
        user = request.data['user']
        text = request.data['text']
        try :
            user = User.objects.get(id = user)
            comment = Comment(user = user , text = text) 
            comment.save()
        
            return Response (ReadCommentSerializer(comment).data)
        except :
            return Response ('error')


class Fav(generics.ListCreateAPIView):
    serializer_class = FavSerializer
    queryset = Favorite.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend , SearchFilter , OrderingFilter]

    filterset_fields = ['patient__id'] #go to home or not 
    search_fields = ['patient__id']



    def post(self, request, *args, **kwargs) :
        try :
            patient = request.data['patient']
            special = request.data['special']
            patient =PatientProfile.objects.get(id =patient)
            special = SpecialistProfile.objects.get(id =special )
        
            fav = Favorite(patient = patient , specialist = special)
            fav.save()
            return Response(FavSerializer(fav).data)
        except :
                return Response('error')



class Fav_pk (generics.DestroyAPIView):
    serializer_class = FavSerializer
    queryset = Favorite.objects.all()


class Comments_pk (generics.RetrieveUpdateDestroyAPIView):

    queryset = Comment.objects.all()
    serializer_class = ReadCommentSerializer




class Appointment_pk (generics.DestroyAPIView) :

    queryset = Appointment.objects.all()
    def delete(self, request, *args, **kwargs):
        try :
            pk=self.kwargs.get('pk')
            app = Appointment.objects.get(pk=pk)
            #### send notification to special 
            specialname = app.specialist.user.username
            special_fcm_token = app.specialist.user.fcm_token
            patientname = app.patient.user.username
            starttime = app.start
            endtime = app.end
            msg = f'{patientname} has cancel appiment in {app.date} at {starttime} to {endtime}'
            UserComponent.sendNotification(msg= msg, title='booking cancel' , token=special_fcm_token)



            app.delete()
            return Response(special_fcm_token)
        except : 
            return Response('error')




class AddFcmToken (generics.CreateAPIView):

    def post (self, request, *args, **kwargs):
        try :
            id = request.data['id']
            token = request.data['token']

            user = User.objects.get(id=id)
            user.fcm_token = token
            user.save()
            return Response('ok')
        except :
            return Response('error')


from django.db.models import Avg
class Recommendation (generics.CreateAPIView) :
    serializer_class = ReadSpecialistSerializer

    filter_backends = [django_filters.rest_framework.DjangoFilterBackend , SearchFilter , OrderingFilter]

    #ordering_fields = ['']
    ordering = ['user__username']
    def post (self, request, *args, **kwargs): 
        id = request.data['id']
        patient = PatientProfile.objects.get(id = id)
        ill = patient.chronic_illness.all()
        ill = ill[0].special_type

        #ChronicIllness.objects.get(name = ill[0])
        print(ill)
        city = patient.user.city

        list1 = SpecialistProfile.objects.select_related('user').all()
        list2 = SpecialistProfile.objects.filter(user__city =city , medical_type = ill ).annotate(avg_rating=Avg('rates__stars')).order_by('avg_rating')
        list1 = list1.exclude(user__city =city , medical_type = ill)
        list3 = list1.filter(medical_type = ill).annotate(avg_rating=Avg('rates__stars')).order_by('avg_rating')
        list1 = list1.exclude(medical_type = ill)
        list4 = list1.filter(user__city = city).annotate(avg_rating=Avg('rates__stars')).order_by('avg_rating')
        list1 = list1.exclude(user__city = city).annotate(avg_rating=Avg('rates__stars')).order_by('avg_rating')

        print(list2)
        print(list3)
        print(type(list4))
        print(list2[0].user.username)
        list2 =list(list2)+list(list3)+list(list4)

        

        return Response(ReadSpecialistSerializer(list2 , many = True).data)



class Notify(generics.ListCreateAPIView):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend , SearchFilter , OrderingFilter]
    filterset_fields = ['user__email'] #go to home or not 
    #search_fields = ['user__username']
    #ordering_fields = ['created_at']
    ordering = ['-created_at']


    def post (self, request, *args, **kwargs)  :
        user = request.data['user']
        msg = request.data['msg']
        title = request.data['title']
        user = User.objects.get(id = user)
        notification = Notification(user = user , msg = msg  , title = title)
        notification.save()
        return Response(NotificationSerializer(notification).data)


class Notify_delete (generics.CreateAPIView) :
    def post(self, request, *args, **kwargs) :
        user = request.data['user']
        user = User.objects.get(id= user)
        notification = Notification.objects.filter(user=user)
        notification.delete()
        return Response('its deleted')

class delete_notify_specific(generics.CreateAPIView):
        def post(self, request, *args, **kwargs) :
            not_id = request.data['id']
            notification = Notification.objects.get(id= not_id)
            
            notification.delete()
            return Response('its deleted')

    






class Appoiment_change_status_done(generics.CreateAPIView) : 
    def post (self, request, *args, **kwargs)  :
        appoimnet_id = request.data['id']
        appoiment = Appointment.objects.get(pk=appoimnet_id)
        appoiment.status = 'done'
        appoiment.save()

        UserComponent.sendNotification(msg= f'hello {appoiment.patient.user.username} you can rate {appoiment.specialist.user.username}', title=f'rating specialist - {appoiment.specialist.user.username} ' , token=appoiment.patient.user.fcm_token)
        notify = Notification(title = f'hello {appoiment.patient.user.username} you can rate {appoiment.specialist.user.username}' , msg =f'rating specialist - {appoiment.specialist.user.username} ' ,user =  appoiment.patient.user )
        notify.save()
        return Response(appoiment.patient.user.fcm_token)

        
        

class Appoiment_change_status_cancel(generics.CreateAPIView) : 
    def post (self, request, *args, **kwargs)  :
        appoimnet_id = request.data['id']
        appoiment = Appointment.objects.get(pk=appoimnet_id)
        appoiment.status = 'cancelled'
        appoiment.save()

        patient_token = appoiment.patient.user.fcm_token
        special_token = appoiment.patient.user.fcm_token
        if patient_token == None :
            patient_token = ''
        
        if special_token == None : 
            special_token = ''
        
        UserComponent.sendNotification(msg= f'the appoiment with {appoiment.specialist.user.username} has been canceled that was specified on {appoiment.date} from {appoiment.start} to {appoiment.end} ', title=f'booking cancel ' , token=patient_token)
        UserComponent.sendNotification(msg= f'the appoiment with {appoiment.specialist.user.username} has been canceled that was specified on {appoiment.date} from {appoiment.start} to {appoiment.end} ', title=f'booking cancel ' , token=special_token)
        notify = Notification(title = f'the appoiment with {appoiment.specialist.user.username} has been canceled that was specified on {appoiment.date} from {appoiment.start} to {appoiment.end} ' , msg =f'booking cancel ' ,user =  appoiment.patient.user )
        notify.save()
        notify1 = Notification(title = f'the appoiment with {appoiment.specialist.user.username} has been canceled that was specified on {appoiment.date} from {appoiment.start} to {appoiment.end} ' , msg =f'booking cancel ' ,user =  appoiment.specialist.user )

        notify1.save()
        

        


        return Response('its cancelled')



class Recommendation_chat_bot (generics.CreateAPIView) :
    serializer_class = ReadSpecialistSerializer

    filter_backends = [django_filters.rest_framework.DjangoFilterBackend , SearchFilter , OrderingFilter]

    #ordering_fields = ['']
    ordering = ['user__username']
    def post (self, request, *args, **kwargs): 
        id = request.data['id']
        patient = PatientProfile.objects.get(id = id)
        ill = patient.chat_bot
        ill = ill.special_type

        #ChronicIllness.objects.get(name = ill[0])
        print(ill)
        city = patient.user.city

        list1 = SpecialistProfile.objects.select_related('user').all()
        list2 = SpecialistProfile.objects.filter(user__city =city , medical_type = ill ).annotate(avg_rating=Avg('rates__stars')).order_by(F('avg_rating').desc(nulls_last=True))
        list1 = list1.exclude(user__city =city , medical_type = ill)
        list3 = list1.filter(medical_type = ill).annotate(avg_rating=Avg('rates__stars')).order_by(F('avg_rating').desc(nulls_last=True))
        list1 = list1.exclude(medical_type = ill)
        list4 = list1.filter(user__city = city).annotate(avg_rating=Avg('rates__stars')).order_by(F('avg_rating').desc(nulls_last=True))
        list1 = list1.exclude(user__city = city).annotate(avg_rating=Avg('rates__stars')).order_by(F('avg_rating').desc(nulls_last=True))

        print(list2)
        print(list3)
        print(type(list4))
        
        list2 =list(list2)+list(list3) #+list(list4)

        

        return Response(ReadSpecialistSerializer(list2 , many = True).data)




    

from django.db.models import F  

class Recommendation_special (generics.CreateAPIView) :
    serializer_class = ReadSpecialistSerializer

    filter_backends = [django_filters.rest_framework.DjangoFilterBackend , SearchFilter , OrderingFilter]

    #ordering_fields = ['']
    ordering = ['user__username']
    def post (self, request, *args, **kwargs): 
        id = request.data['id']
        type1 = request.data['type']
        patient = PatientProfile.objects.get(id = id)
        ill = patient.symptoms
        ill = Symptoms.objects.filter( name= patient.symptoms)
        print(ill)
        #ill = ill.special_type
        #ill = ill[1].special_type
        print(ill)
        if type1 =='NURSE':
            ill = ill[1].special_type
        if type1 =='DOCTOR':
            ill = ill[0].special_type



        #ChronicIllness.objects.get(name = ill[0])
        
        city = patient.user.city

        list1 = SpecialistProfile.objects.select_related('user').filter(type = type1)
        if (type1 =='PHYSICIAN' or	type1 =='ELDERLY_CARE' or type1=='BABY_CARE' ):
            list5 = list1.filter(user__city = city  ).annotate(avg_rating=Avg('rates__stars')).order_by(F('avg_rating').desc(nulls_last=True))
            return Response(ReadSpecialistSerializer(list5 , many = True).data)

           
        else :
          
            list2 = SpecialistProfile.objects.filter(user__city =city , medical_type = ill ).annotate(avg_rating=Avg('rates__stars')).order_by(F('avg_rating').desc(nulls_last=True))

        list1 = list1.exclude(user__city =city , medical_type = ill )
        list3 = list1.filter(medical_type = ill ).annotate(avg_rating=Avg('rates__stars')).order_by(F('avg_rating').desc(nulls_last=True))
        list1 = list1.exclude(medical_type = ill )
        list4 = list1.filter(user__city = city  ).annotate(avg_rating=Avg('rates__stars')).order_by(F('avg_rating').desc(nulls_last=True))
        list1 = list1.exclude(user__city = city ).annotate(avg_rating=Avg('rates__stars')).order_by(F('avg_rating').desc(nulls_last=True))

        print(list2)
        print(list3)
        print(type(list4))
        #print(list2[0].user.username)
        list2 =list(list2)+list(list3)+list(list4)

        

        return Response(ReadSpecialistSerializer(list2 , many = True).data)


class how_i_am_talk(generics.CreateAPIView) :

    def post (self, request, *args, **kwargs) :
        chat = []
        email = request.data['email']
        #type1 = request.data['type']
        user=    UserComponent.how_iam_talk(email)
        print(user)
        for x in user:
                user = User.objects.get(email = x)
                chat.append(user)
        return Response(ReadUserMiniInfoSerializer(chat , many =True).data)

               


        if type1 =='special':
            for x in user:
                patient = PatientProfile.objects.get(user__email = email)
                chat.append(patient)
            
            return Response(ReadPatientSerializer(chat , many =True).data)

        if type1 =='patient':
                for x in user:
                    special = SpecialistProfile.objects.get(user__email = email)
                    chat.append(special)
                return Response(ReadSpecialistSerializer(chat , many =True).data)
        
        return Response('error')


class Complemnt_fav (generics.CreateAPIView):

    def post(self, request, *args, **kwargs):
        id = request.data['id']
        id1 = request.data['id1']
        special = SpecialistProfile.objects.get(id = id)
        special.Fav = not special.Fav 
        special.save()
        patient =PatientProfile.objects.get(id = id1)
        if special.Fav ==True :
            fav = Favorite(patient = patient , specialist = special)
            fav.save()
        
        if special.Fav == False :
            fav = Favorite.objects.get(patient = patient , specialist = special)
            fav.delete()

        return Response('ok')

class convert_corona(generics.CreateAPIView)  :
    def post(self, request, *args, **kwargs):

        
        patient = PatientProfile.objects.get(id=5)
        patient.chat_bot = ChronicIllness.objects.get(id=2)
        patient.save()
        return Response('ok')

class convert_nothing(generics.CreateAPIView)  :
    def post(self, request, *args, **kwargs):

        
        patient = PatientProfile.objects.get(id=5)
        patient.chat_bot = ChronicIllness.objects.get(id=3)
        print(patient.chat_bot.name)
        patient.save()
        return Response('ok')
    
                
        


            
