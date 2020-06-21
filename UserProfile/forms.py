from django import forms
from .models import Profile
from django.core.exceptions import ValidationError
import re
from django.contrib.auth import authenticate


class ProfileForm(forms.Form):
    about = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}) )
    birth_date = forms.DateField(widget=forms.SelectDateWidget(attrs={'class': 'form-control'}, years=list(range(1900, 2020))))
    email = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    city = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    interests = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}))
    avatar = forms.ImageField(required=False)


    def get_about(self):
        return self.cleaned_data['about']

    def get_birth_date(self):
        return self.cleaned_data['birth_date']

    def get_email(self):
        return self.cleaned_data['email']

    def get_city(self):
        return self.cleaned_data['city']

    def get_phone(self):
        return self.cleaned_data['phone']

    def get_interests(self):
        return self.cleaned_data['interests']

    def get_avatar(self):
        return self.cleaned_data['avatar']

    def change_profile(self, user, avatar):
        profile = user.profilet
        self.clean()
        profile.about = self.get_about()
        profile.birth_date = self.get_birth_date()
        profile.email = self.get_email()
        profile.city = self.get_city()
        profile.phone = self.get_phone()
        profile.interests = self.get_interests()
        if self.get_avatar() is not None:
            profile.avatar = self.get_avatar()
        profile.save()


class PrivacySettingsForm(forms.Form):
    allow_to_view_for_unreg = forms.BooleanField(required=False)

    def get_allow_view_unreg(self):
        return self.cleaned_data['allow_to_view_for_unreg']

    def change_privacy_settings(self, user):
        privacy_settings = user.profile.privacysettings
        self.clean()
        privacy_settings.allow_to_view_for_unreg = self.get_allow_view_unreg()
        privacy_settings.save()


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(max_length=32, widget=forms.PasswordInput())
    confirm_password = forms.CharField(max_length=32, widget=forms.PasswordInput())
    new_password = forms.CharField(max_length=32, widget=forms.PasswordInput())

    old_password.widget.attrs.update({'class': 'form-control'})
    new_password.widget.attrs.update({'class': 'form-control'})
    confirm_password.widget.attrs.update({'class': 'form-control'})

    def clean_new_password(self):
        temp_confirm_password = self.cleaned_data['confirm_password']
        temp_new_password = self.cleaned_data['new_password']
        temp_old_password = self.cleaned_data['old_password']

        userexp = re.compile('^[A-Za-z0-9_-]{8,100}$')

        if len(temp_new_password) < 8:
            raise ValidationError("Минимальная длина пароля - 8.")

        if len(temp_new_password) > 100:
            raise ValidationError("Максимальная длина пароля - 100.")

        if temp_new_password != temp_confirm_password:
            raise ValidationError("Пароли не совпадают.")

        if not userexp.match(temp_new_password):
            raise ValidationError("В пароле могут присутствовать лишь английские буквы, цифры, дефис и знак подчёркивания")

        if temp_old_password == temp_new_password:
            raise ValidationError('Старый пароль совпадает с новым')

        return temp_new_password

    def change_password(self, user):
        check_user = authenticate(username=user.username, password=self.cleaned_data['old_password'])
        if check_user is not None:
            user.set_password(self.cleaned_data['new_password'])
            user.save()
            return True
        else:
            return False



