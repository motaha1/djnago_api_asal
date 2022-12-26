# from datetime import timedelta
#
# from django.conf import settings
# from django.utils import timezone
# from django.utils.translation import ugettext_lazy as _
# from rest_framework import exceptions
#
# from core.constants.email_content_messages import EmailMessages
# from core.apps.users.constants import UserVerificationTokenType, VerificationTokenStatus
# from core.users.models import User, UserVerificationToken
# from helpers.general_helper import generate_random_token
# from helpers.mailing_helper import EmailHelper
#
#
# class AuthComponent:
#     @staticmethod
#     def handle_forget_password(email: str):
#         try:
#             user = User.objects.get(email=email)
#             token_obj = UserVerificationToken.objects.create(user=user, token=generate_random_token(),
#                                                              token_type=UserVerificationTokenType.RESET_PASSWORD)
#             reset_password_link = "{base_link}{path}{token}".format(base_link=settings.CELERO_FE_URL,
#                                                                     path="/reset-password/", token=token_obj.token)
#             email_text = EmailMessages.FORGET_PASSWORD_EMAIL.format(
#                 receiver_name=user.get_full_name(),
#                 link=reset_password_link)
#             EmailHelper.send_simple_html_email(from_email=settings.CELERO_TEAM_EMAIL, to_emails=[user.email],
#                                                subject="Reset Password", text_content=email_text)
#         except User.DoesNotExist:
#             return
#
#     @staticmethod
#     def handle_reset_password(token, new_password):
#         verification_token = UserVerificationToken.objects.filter(token=token,
#                                                                   status=VerificationTokenStatus.ACTIVE,
#                                                                   token_type=UserVerificationTokenType.RESET_PASSWORD).last()
#         if not verification_token:
#             raise exceptions.ValidationError(_("Invalid Token"))
#
#         user = verification_token.user
#         token_expiry_date = timedelta(minutes=verification_token.expire_after) + verification_token.created_at
#         if token_expiry_date < timezone.now():
#             raise exceptions.ValidationError(_("Invalid Token"))
#         # update password
#         verification_token.status = VerificationTokenStatus.INACTIVE
#         verification_token.save()
#         user.set_password(raw_password=new_password)
#         user.save()
