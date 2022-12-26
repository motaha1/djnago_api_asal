from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class AskCareCustomPasswordValidator:

    def __init__(self, min_length=1):
        self.min_length = min_length

    def validate(self, password, user=None):
        if not any(char.isdigit() for char in password):
            raise ValidationError(
                _('Password must contain at least %(min_length)d digit.') % {'min_length': self.min_length})
        if not any(char.isalpha() for char in password):
            raise ValidationError(
                _('Password must contain at least %(min_length)d letter.') % {'min_length': self.min_length})

        if not any(str(char).islower() for char in password):
            raise ValidationError(
                _('Password must contain at least %(min_length)d lower case Character.') % {
                    'min_length': self.min_length})

        if not any(str(char).isupper() for char in password):
            raise ValidationError(
                _('Password must contain at least %(min_length)d upper case Character.') % {
                    'min_length': self.min_length})

    def get_help_text(self):
        return "Password must contain both letters and digits, at least 1 lower-case letter and at least 1 upper-case letter"
