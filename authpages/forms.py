from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.validators import validate_email
import re

class LoginForm(forms.Form):
    login = forms.CharField(max_length=16)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput())

    login.widget.attrs.update({'class':'form-control'})
    password.widget.attrs.update({'class':'form-control'})

    def clean_password(self):
        temp_login = self.cleaned_data['login'].lower()
        temp_password = self.cleaned_data['password']

        user = authenticate(username=temp_login, password=temp_password)

        if user is None:
            raise ValidationError("Комбинация логин+пароль не подходит.")

        return temp_password

    def DoAuth(self):
        user = authenticate(username=self.cleaned_data['login'], password=self.cleaned_data['password'])
        return user


class RegistrationForm(forms.Form):
    login = forms.CharField(max_length=64)
    email = forms.CharField(max_length=32)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput())
    confirmpass = forms.CharField(max_length=32, widget=forms.PasswordInput())

    login.widget.attrs.update({'class':'form-control'})
    email.widget.attrs.update({'class':'form-control'})
    password.widget.attrs.update({'class':'form-control'})
    confirmpass.widget.attrs.update({'class':'form-control'})
    login.widget.attrs.update({'autocomplete':'off'})
    email.widget.attrs.update({'autocomplete':'off'})
    password.widget.attrs.update({'autocomplete':'new-password'})
    confirmpass.widget.attrs.update({'autocomplete':'new-password'})

    def clean_confirmpass(self):
        temp_confirmpass = self.cleaned_data['confirmpass']
        temp_password = self.cleaned_data['password']

        userexp = re.compile('^[A-Za-z0-9_-]{8,100}$')

        if len(temp_password) < 8:
            raise ValidationError("Минимальная длина пароля - 8.")

        if len(temp_password) > 100:
            raise ValidationError("Максимальная длина пароля - 100.")

        if temp_confirmpass != temp_password:
            raise ValidationError("Пароли не совпадают.")

        if not userexp.match(temp_password):
            raise ValidationError("В пароле могут присутствовать лишь английские буквы, цифры, дефис и знак подчёркивания")


        return temp_confirmpass

    def clean_login(self):
        temp_login = self.cleaned_data['login']

        userexp = re.compile('^[a-z0-9_-]{3,20}$')

        if len(temp_login) < 3:
            raise ValidationError("Минимальная длина логина - 3.")
        elif len(temp_login) > 20:
            raise ValidationError("Максимальная длина логина - 20.")

        if not userexp.match(temp_login):
            raise ValidationError("В имени пользователя могут присутствовать лишь английские строчные буквы, цифры, дефис и знак подчёркивания")

        if User.objects.filter(username=temp_login).count() != 0:
            raise ValidationError("Пользователь с таким именем уже зарегистрирован.")

        return temp_login

    def clean_email(self):
        temp_email = self.cleaned_data['email']

        if User.objects.filter(email=temp_email).count() != 0:
            raise ValidationError("Пользователь с такой почтой уже зарегистрирован.")
        try:
            validate_email(temp_email)
            valid_email = True
        except ValidationError:
            valid_email = False

        if not valid_email:
            raise ValidationError("В написании адреса почты допущена ошибка.")

        return temp_email

    def DoRegister(self):
        user = User.objects.create_user(self.cleaned_data['login'], self.cleaned_data['email'], self.cleaned_data['password'])
        user.save()
        return user
