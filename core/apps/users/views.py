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
    ReadUserMiniInfoSerializer, ReadSpecialistSerializer, ReadPatientSerializer, WritePatientSerializer


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


class SpecialistCreateAPIView(generics.CreateAPIView):
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
