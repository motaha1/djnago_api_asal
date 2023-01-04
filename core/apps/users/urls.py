from django.urls import path

from core.apps.users.views import PatientCreateAPIView, SpecialistCreateAPIView, UpdateUserAvatarView, \
    RetrieveOrUpdateSpecialistAPIView, RetrieveOrUpdatePatientAPIView, ListBloodTypeAPIView, \
    ListMedicalTypeAPIView, ListSpecialistTypeAPIView, ListCollegesDegreesAPIView , AllSpecialList , RattingView , AppointmentWrite ,Appointmentview , Otpverify , AllPatient, login , chat ,palestineId , \
        sendNotification , Comments , Fav , Fav_pk, Comments_pk , Appointment_pk , Recommendation

URLS = [
    path(r'patients', PatientCreateAPIView.as_view()),
    path(r'specialists', SpecialistCreateAPIView.as_view()),
    path(r'<int:user_id>/avatar', UpdateUserAvatarView.as_view()),
    path(r'specialists/<int:specialist_id>', RetrieveOrUpdateSpecialistAPIView.as_view()),
    path(r'patients/<int:patient_id>', RetrieveOrUpdatePatientAPIView.as_view()),
#
    path(r'allspeciallist/', AllSpecialList.as_view()),
    path(r'allpatient/', AllPatient.as_view()),

    path(r'addratting/', RattingView.as_view()),
    path(r'addappoiment/', AppointmentWrite.as_view()),
    path(r'viewappoiment/', Appointmentview.as_view()),
    path(r'appoiment/<pk>', Appointment_pk.as_view()),


    
    path(r'otpverify/', Otpverify.as_view()),
    path(r'login/', login.as_view()),
    
    path(r'chat/', chat.as_view()),
    path(r'palestineid/', palestineId.as_view()),
    path(r'sendnotification/', sendNotification.as_view()),
   
    path(r'comments/', Comments.as_view()),

    path(r'comments/<pk>', Comments_pk.as_view()),
    path(r'fav/', Fav.as_view()),
    path(r'fav/<pk>', Fav_pk.as_view()),

    
    path(r'rec/', Recommendation.as_view()),

    




    



    # ---------------------- Lookups ------------------#
    path(r'lookups/blood-types', ListBloodTypeAPIView.as_view()),
    path(r'lookups/medical-types', ListMedicalTypeAPIView.as_view()),
    path(r'lookups/specialist-types', ListSpecialistTypeAPIView.as_view()),
    path(r'lookups/colleges-degrees', ListCollegesDegreesAPIView.as_view()),

   


    # path(r'me/', UserRetrievePersonalInfoAPIView.as_view()),
    # path(r'verify-email/', UserVerifyEmailAPIView.as_view()),
    # path(r'<int:user_id>/password/', ChangeUserPasswordView.as_view())
]
