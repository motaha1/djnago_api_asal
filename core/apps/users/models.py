import uuid
from collections import OrderedDict
from uuid import uuid4

from django.core.validators import validate_email
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager
from django.db.models import Q
import time

from rest_framework.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from core.apps.abstract_models import AskCareBaseModel
from core.apps.users.constants import UserType, Gender, BloodType, SpecialistType, CollegesDegrees, MedicalType

from django.core.validators import RegexValidator

# from core.helpers.s3_helper import UserAvatarMediaStorage, avatars_directory_path

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                             message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")


class UserMedia(AskCareBaseModel):
    profile_img = models.ImageField(upload_to='media/', null=True)


class User(AbstractBaseUser, PermissionsMixin, AskCareBaseModel):
    email = models.EmailField(_('email address'), max_length=225, unique=True, blank=False)  # required
    username = models.CharField(_('username'), max_length=225, unique=True, blank=False)  # required
    gender = models.CharField(_('gender'), choices=Gender.choices, max_length=10, null=True)  # not required
    mobile = models.CharField(_('mobile'), validators=[phone_regex], max_length=17, blank=False,
                              null=True)  # not required
    city = models.CharField(_('location'), max_length=100, null=True)  # required
    birthdate = models.DateField(_('birth date'), null=True)  # required
    avatar = models.OneToOneField(UserMedia,
                                  blank=True,
                                  null=True,
                                  related_name="user",
                                  related_query_name="user",
                                  on_delete=models.DO_NOTHING)

    is_staff = models.BooleanField(_('staff'), default=False)
    is_active = models.BooleanField(_('active'), default=False)
    is_patient = models.BooleanField(_('is patient'), default=False)
    is_specialist = models.BooleanField(_('is specialist'), default=False)
    fcm_token = models.CharField(max_length=100000 , blank=True , null=True )

    objects = UserManager()
    REQUIRED_FIELDS = ['username', 'password']
    USERNAME_FIELD = 'email'

    class Meta:
        db_table = 'users'
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.username

    def save(self, *args, **kwargs):
        try:
            validate_email(self.email)
        except Exception:
            raise ValidationError("Invalid Email")

        if not self.pk:
            if not self.username:
                index_of_at = self.email.index('@')
                # if no user_name, extract email part befor the @ and append current time milliseconds to insure
                # uniqueness
                self.username = f"{self.email[0:index_of_at]}{str(int(time.time() * 1000))[-5:]}"

        super(User, self).save(*args, **kwargs)


class ChronicIllness(models.Model):
    name = models.CharField(_('chronic illness name'), max_length=100, null=False, blank=False, unique=True)


class PatientProfile(AskCareBaseModel):
    user = models.OneToOneField(User,
                                blank=False,
                                null=False,
                                related_name="patients",
                                related_query_name="patient",
                                on_delete=models.CASCADE)

    blood_type = models.CharField(_('blood type'), choices=BloodType.choices, max_length=10, null=True)  # not required
    chronic_illness = models.ManyToManyField(ChronicIllness, blank=True, null=True)
    have_allergies = models.BooleanField(_('have allergies'), default=False)

    otp = models.CharField(max_length=200 , null=True , blank=True)  ####new 


class SpecialistProfile(AskCareBaseModel):
    user = models.OneToOneField(User,
                                blank=False,
                                null=False,
                                related_name="specialists",
                                related_query_name="specialist",
                                on_delete=models.CASCADE)
    type = models.CharField(_('type'), choices=SpecialistType.choices, max_length=50, null=False)  # required
    hour_cost = models.PositiveIntegerField(_('specialist hour cost'), null=True)
    daily_open_from = models.TimeField(_('open from'), null=True)
    daily_open_to = models.TimeField(_('open_to'), null=True)
    top_degree = models.CharField(_('top degree'), choices=CollegesDegrees.choices, max_length=100, null=True)
    examination_avg_period = models.PositiveIntegerField(_('examination avg time'), default=15)  # in mins
    job_title = models.CharField(_('job'), max_length=225, blank=True)

    ####new ##
    allow_Messages = models.BooleanField(default=True)
    allow_booking = models.BooleanField(default=True)



    @property
    def get_avg(self):
        pass
        #return Rating.objects.filter(nurse = self).count()





class Symptoms(models.Model):
    name = models.CharField(_('symptoms name'), max_length=100, null=False, blank=False, unique=True)


class Appointment(AskCareBaseModel):
    specialist = models.ForeignKey(SpecialistProfile, blank=False, null=True, on_delete=models.CASCADE)
    patient = models.ForeignKey(PatientProfile, blank=False, null=True, on_delete=models.CASCADE)
    start = models.CharField(null=True  ,max_length=50 )
    end = models.CharField(null=True ,max_length=50)
    date = models.CharField(null=True ,max_length=50 )
    #%y/%m/%d

    # status = models.CharField(_('appointment status'), choices=AppointmentStatus.choices, max_length=50,
    # null=False, default=)

    # class Meta:
    #     unique_together = [['specialist', 'patient', 'time']]


#### new added######

from django.core.validators import MaxValueValidator, MinValueValidator

class Ratting (AskCareBaseModel):
    specialist = models.ForeignKey(SpecialistProfile, blank=False, null=False, on_delete=models.CASCADE)
    patient = models.ForeignKey(PatientProfile, blank=False, null=False, on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    comment = models.CharField(max_length=1000 , blank = True , null = True )



class Comment(AskCareBaseModel) :
    user = models.ForeignKey(User , on_delete= models.CASCADE , blank= False , null= False)
    text = models.TextField(null=False , blank=False)


class Favorite(models.Model) :
    specialist = models.ForeignKey(SpecialistProfile, blank=False, null=False, on_delete=models.CASCADE)
    patient = models.ForeignKey(PatientProfile, blank=False, null=False, on_delete=models.CASCADE)

