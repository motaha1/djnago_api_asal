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
        FavSerializer

from core.apps.users.models import *
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist



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
    queryset = SpecialistProfile.objects.all()
    serializer_class = ReadSpecialistSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend , SearchFilter , OrderingFilter]
    #filter_fields =('type')
    filterset_fields = ['type' , 'user__email' ] #go to home or not 
    search_fields = ['user__username']
    ordering_fields = ['user__username', 'user__email']
    ordering = ['user__username']

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

class Appointmentview (generics.ListAPIView):

     serializer_class = ReadAppointmentSerializer
     queryset = Appointment.objects.all()
     filter_backends = [django_filters.rest_framework.DjangoFilterBackend , SearchFilter , OrderingFilter]
     filterset_fields = ['specialist__id',  'specialist__user__username','specialist__user__email','patient__user__username' , 'date', 'patient__user__email' ,'patient__id']

     

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


        UserComponent.chat(sender=sender , receiver=receiver , time=time , text=text)

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








    



