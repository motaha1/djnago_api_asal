from django.urls import path

from core.apps.users.views import PatientCreateAPIView, SpecialistCreateAPIView, UpdateUserAvatarView, \
    RetrieveOrUpdateSpecialistAPIView, RetrieveOrUpdatePatientAPIView, ListBloodTypeAPIView, \
    ListMedicalTypeAPIView, ListSpecialistTypeAPIView, ListCollegesDegreesAPIView

URLS = [
    path(r'patients', PatientCreateAPIView.as_view()),
    path(r'specialists', SpecialistCreateAPIView.as_view()),
    path(r'<int:user_id>/avatar', UpdateUserAvatarView.as_view()),
    path(r'specialists/<int:specialist_id>', RetrieveOrUpdateSpecialistAPIView.as_view()),
    path(r'patients/<int:patient_id>', RetrieveOrUpdatePatientAPIView.as_view()),

    # ---------------------- Lookups ------------------#
    path(r'lookups/blood-types', ListBloodTypeAPIView.as_view()),
    path(r'lookups/medical-types', ListMedicalTypeAPIView.as_view()),
    path(r'lookups/specialist-types', ListSpecialistTypeAPIView.as_view()),
    path(r'lookups/colleges-degrees', ListCollegesDegreesAPIView.as_view()),

    # path(r'me/', UserRetrievePersonalInfoAPIView.as_view()),
    # path(r'verify-email/', UserVerifyEmailAPIView.as_view()),
    # path(r'<int:user_id>/password/', ChangeUserPasswordView.as_view())
]
