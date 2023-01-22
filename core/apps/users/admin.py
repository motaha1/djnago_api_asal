import django
from django import forms
from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, UserAdmin
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.contrib.auth.forms import UserCreationForm

from core.apps.users.constants import InternalCustomAdminActions
from core.apps.users.models import *

# from .models import User
from core.apps.users.models import User, ChronicIllness, PatientProfile, SpecialistProfile, Symptoms, Appointment , UserMedia


class CustomAdminPasswordChangeForm(AdminPasswordChangeForm):

    def save(self, commit=True):
        """
        add new attribute for user objects, this is to be used in signal (users/signal.py( to sync with auth0
        """
        self.user.action = InternalCustomAdminActions.ADMIN_CHANGE_USER_PASSWORD
        self.user._raw_password = self.cleaned_data['password1']
        super().save(commit=commit)


class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"


class UserAdminFormAdd(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'mobile')


# Register your models here.
@django.contrib.admin.register(User)
class UserAdmin(BaseUserAdmin):
    change_password_form = CustomAdminPasswordChangeForm
    change_form_template = "admin/users/user/change_form.html"

    form = UserAdminForm
    add_form = UserAdminFormAdd
    list_display = (
        'username', 'email', 'is_active', 'is_staff', 'is_patient', 'is_specialist')
    exclude = ('user_permissions', 'groups')

    # for fields to be used in editing users
    fieldsets = (
        (None,
         {'fields': (
             'email', 'username', 'gender', 'is_active', 'is_staff', 'is_patient', 'is_specialist',
             'city', 'birthdate', 'mobile' , 'avatar1' , 'fcm_token' , 'password')}),
    )

    # for fields to be used when creating a user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'mobile'),
        }),
    )
    search_fields = ('email', 'username')
    list_editable = ('is_active' , )
    list_filter = ('is_staff', 'is_superuser', 'groups', 'is_staff', 'is_patient', 'is_specialist')
    ordering = ('-created_at',)

    def has_delete_permission(self, request, obj=None):
        return False

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['user_id'] = object_id
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )

########################register patient ###################################




class SpecialistAdminForm(forms.ModelForm):
    class Meta:
        model = SpecialistProfile
        fields = "__all__"



@django.contrib.admin.register(SpecialistProfile)
class SpecialistProfileAdmin(admin.ModelAdmin):
    change_password_form = CustomAdminPasswordChangeForm
    change_form_template = "admin/users/user/change_form.html"

    form = SpecialistAdminForm
    #add_form = UserAdminFormAdd
    search_fields = ['user__username']
    list_display = ('user'  ,
       'type', 'top_degree' , 'name' , 'is_active')
    exclude = ('user_permissions', 'groups')
    def name (self , object) : 
        return object.user.username
    
    def is_active(self , object)  :
        return object.user.is_active 
    
    
    

    # for fields to be used in editing users
    # fieldsets = (
    #     (None,
    #      {'fields': (
    #          'email', 'username', 'gender', 'is_active', 'is_staff', 'is_patient', 'is_specialist',
    #          'city', 'birthdate', 'mobile')}),
    # )

    # for fields to be used when creating a user
    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('email', 'username', 'password1', 'password2', 'mobile'),
    #     }),
    # )

    list_filter = ('type', 'top_degree')



    def has_delete_permission(self, request, obj=None):
        return False

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['user_id'] = object_id
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )


# admin.site.register(PatientProfile)
# admin.site.register(SpecialistProfile)
# admin.site.register(Ratting)




# @django.contrib.admin.register(PatientProfile)
# class PatientProfileAdmin(BaseUserAdmin):
#     def has_delete_permission(self, request, obj=None):
#         return False


# @django.contrib.admin.register(SpecialistProfile)
# class SpecialistProfileAdmin(BaseUserAdmin):
#     def has_delete_permission(self, request, obj=None):
#         return False


# admin.register(ChronicIllness)
# admin.register(Symptoms)

admin.site.register(Appointment)
admin.site.register(Comment)
admin.site.register(PatientProfile)
admin.site.register(ChronicIllness)
admin.site.register(UserMedia)
#admin.site.register(UserMedia)
admin.site.register(Notification)
admin.site.register(Symptoms)
admin.site.register(Favorite)
admin.site.register(Ratting)







from django.contrib.auth.models import Group
admin.site.unregister(Group)

admin.site.site_header = "Ask For Care Adminpanel"
admin.site.site_title = "Ask For Care Adminpanel"




