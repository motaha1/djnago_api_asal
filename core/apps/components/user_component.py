from logging import getLogger
from django.db import IntegrityError
from rest_framework.exceptions import NotFound, ValidationError, PermissionDenied

from core.apps.users.constants import InternalCustomAdminActions
from core.apps.users.models import PatientProfile, User, SpecialistProfile, UserMedia

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


