from django import forms
from .models import Profile
from django.core.exceptions import ValidationError
import re
from django.contrib.auth import authenticate


class ProfileForm(forms.Form):
    about = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}), required=False)
    birth_date = forms.DateField(widget=forms.SelectDateWidget(attrs={'class': 'form-control'}, years=list(range(1900, 2020))), required=False)
    email = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    city = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    phone = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    interests = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}), required=False)
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

    def clean_phone(self):
        phone = self.get_phone()
        userexp = re.compile('\+[0-9]{8,15}$')
        if not userexp.match(phone):
            if len(phone) < 8:
                raise ValidationError('Минимальная длина номера — 8')
            elif len(phone) > 15:
                raise ValidationError('Максимальная длина номера — 15')
            elif phone[0] != '+':
                raise ValidationError('Номер должен содержать "+" в начале')
            elif not phone[1:].isdigit():
                raise ValidationError('Номер может содержать только цифры и знак "+" в начале')
            else:
                raise ValidationError('Неверный формат номера телефона')
        return phone

    def change_profile(self, user, avatar):
        profile = user.profile
        self.clean()
        if self.get_about() is not None:
            profile.about = self.get_about()
        if self.get_birth_date() is not None:
            profile.birth_date = self.get_birth_date()
        profile.email = self.get_email()
        user.email = self.get_email()
        if self.get_city() is not None:
            profile.city = self.get_city()
        profile.phone = self.get_phone()
        if self.get_interests() is not None:
            profile.interests = self.get_interests()
        if self.get_avatar() is not None:
            profile.avatar = self.get_avatar()
        profile.save()
        user.save()


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



