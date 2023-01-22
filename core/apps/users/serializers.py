from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from core.apps.abstract_models import ReadModelSerializer
from core.apps.users.models import Appointment, User, UserMedia, SpecialistProfile, PatientProfile , Ratting , Comment , Favorite ,Notification
from django.db.models import Avg

# class ChangeUserPasswordSerializer(serializers.Serializer):
#     def create(self, validated_data):
#         pass
#
#     def update(self, instance, validated_data):
#         pass
#
#     password = serializers.CharField(required=True, allow_blank=False)
#
#     def validate_password(self, value):
#         ask_care_validate_password(value)
#

class UserAvatarSerializer(ReadModelSerializer):

    class Meta:
        model = UserMedia
        exclude = ('created_at', 'updated_at')
        # read_only_fields = '__all__'


class ReadUserMiniInfoSerializer(ReadModelSerializer):
    avatar = UserAvatarSerializer(many=False)

    class Meta:
        model = User
        exclude = ('created_at', 'updated_at', 'password', 'groups', 'user_permissions')
        # read_only_fields = '__all__'


class ReadSpecialistSerializer(ReadModelSerializer):
    user = ReadUserMiniInfoSerializer(many=False)

    rattingScore = serializers.SerializerMethodField("apple")

    avg_rating = serializers.FloatField( required = False)
    

    def apple(self , object):
      return  Ratting.objects.filter(specialist = object).aggregate(Avg('stars'))
        

    class Meta:
        model = SpecialistProfile
        fields = '__all__'


class ReadPatientSerializer(ReadModelSerializer):
    user = ReadUserMiniInfoSerializer(many=False)

    class Meta:
        model = PatientProfile
        fields = '__all__'


class WriteUserSerializer(ModelSerializer):
    username = serializers.CharField(validators=[])
    class Meta:
        model = User
        fields = ['username', 'mobile', 'gender', 'city', 'birthdate']


class WriteSpecialistSerializer(ModelSerializer):
    user = WriteUserSerializer(many=False)

    class Meta:
        model = SpecialistProfile
        fields = '__all__'

    def update(self, instance, validated_data):
        user = validated_data.pop('user')
        User.objects.filter(pk=instance.user_id).update(**user)
        instance.__dict__.update(validated_data)
        instance.save(update_fields=validated_data.keys())
        return instance


class WritePatientSerializer(ModelSerializer):
    user = WriteUserSerializer(many=False)

    class Meta:
        model = PatientProfile
        fields = '__all__'

    def update(self, instance, validated_data):
        user = validated_data.pop('user')
        User.objects.filter(pk=instance.user_id).update(**user)
        instance.__dict__.update(validated_data)
        instance.save(update_fields=validated_data.keys())
        return instance

class ReadRatting(ModelSerializer) :
    # specialist = ReadSpecialistSerializer()
    # patient = ReadPatientSerializer()

    class Meta:
        model = Ratting
        fields = '__all__'


class WriteAppointmentSerializer(ModelSerializer) :
        class Meta:
            model = Appointment
            fields = '__all__'


class ReadAppointmentSerializer (ModelSerializer) : 
        specialist = ReadSpecialistSerializer()
        patient = ReadPatientSerializer()

        class Meta:
                model = Appointment
                fields = '__all__'

class ReadCommentSerializer(ModelSerializer) :
    user = ReadUserMiniInfoSerializer()
    class  Meta:
        model = Comment
        fields = '__all__'

# class WriteCommentSerializer(ModelSerializer) :
    
#     class  Meta:
#         model = Comment
#         fields = '__all__'


class FavSerializer(ModelSerializer) :
        specialist = ReadSpecialistSerializer()
        patient = ReadPatientSerializer()
        class  Meta:
            model = Favorite
            fields = '__all__'


class NotificationSerializer(ModelSerializer):
    user = ReadUserMiniInfoSerializer()
    class  Meta:
        model = Notification
        fields = '__all__'