from django.urls import path

from core.apps.users.views import PatientCreateAPIView, SpecialistCreateAPIView, UpdateUserAvatarView, \
    RetrieveOrUpdateSpecialistAPIView, RetrieveOrUpdatePatientAPIView, ListBloodTypeAPIView, \
    ListMedicalTypeAPIView, ListSpecialistTypeAPIView, ListCollegesDegreesAPIView , AllSpecialList , RattingView , AppointmentWrite ,Appointmentview , Otpverify , AllPatient, login , chat ,palestineId , \
        sendNotification , Comments , Fav , Fav_pk, Comments_pk , Appointment_pk , Recommendation , Notify , Notify_delete  ,AddFcmToken , Appoiment_change_status_done , Appoiment_change_status_cancel, Recommendation_chat_bot  ,Recommendation_special , how_i_am_talk , Complemnt_fav , delete_notify_specific , convert_corona , convert_nothing

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

    path(r'appoiment_done/', Appoiment_change_status_done.as_view()),

path(r'rec_chatbot/', Recommendation_chat_bot.as_view()),

    



    
    path(r'otpverify/', Otpverify.as_view()),
    path(r'login/', login.as_view()),
    
    path(r'chat/', chat.as_view()),
    path(r'palestineid/', palestineId.as_view()),
    path(r'sendnotification/', sendNotification.as_view()),

        path(r'how_i_am_talk/', how_i_am_talk.as_view()),

    
   
    path(r'comments/', Comments.as_view()),

    path(r'comments/<pk>', Comments_pk.as_view()),
    
    path(r'fav/', Fav.as_view()),
    path(r'fav/<pk>', Fav_pk.as_view()),

    path(r'comp_fav/', Complemnt_fav.as_view()),

    

    
    path(r'rec/', Recommendation.as_view()),
    path(r'notification/', Notify.as_view()),
    path(r'notification_delete/', Notify_delete.as_view()),
    path(r'addfcm/', AddFcmToken.as_view()),
    path(r'appoiment_cancel/', Appoiment_change_status_cancel.as_view()),
    path(r'appoiment_cancel/', Appoiment_change_status_cancel.as_view()),

    path(r'rec_special/', Recommendation_special.as_view()),

      path(r'notification_delete_specific/', delete_notify_specific.as_view()),
      path(r'convert_corona/', convert_corona.as_view()),
                                                      
      path(r'convert_nothing/', convert_nothing.as_view()),





    




    


    
    




    




    



    # ---------------------- Lookups ------------------#
    path(r'lookups/blood-types', ListBloodTypeAPIView.as_view()),
    path(r'lookups/medical-types', ListMedicalTypeAPIView.as_view()),
    path(r'lookups/specialist-types', ListSpecialistTypeAPIView.as_view()),
    path(r'lookups/colleges-degrees', ListCollegesDegreesAPIView.as_view()),

   


    # path(r'me/', UserRetrievePersonalInfoAPIView.as_view()),
    # path(r'verify-email/', UserVerifyEmailAPIView.as_view()),
    # path(r'<int:user_id>/password/', ChangeUserPasswordView.as_view())
]
