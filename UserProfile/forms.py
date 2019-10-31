from django import forms
from .models import Profile
from django.core.exceptions import ValidationError

class ProfileForm(forms.Form):
    about = forms.CharField(max_length=500)
    birth_date = forms.DateField(widget=forms.SelectDateWidget(years=list(range(1900, 2019))))
    email = forms.CharField(max_length=50)
    city = forms.CharField(max_length=30)
    phone = forms.CharField(max_length=30)
    interests = forms.CharField(max_length=500)

    #Сделать нормальные типы field

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

    #Написать clean-ы

    def change_profile(self, user):
        profile = user.profile
        self.clean()
        profile.about = self.get_about()
        profile.birth_date = self.get_birth_date()
        profile.email = self.get_email()
        profile.city = self.get_city()
        profile.phone = self.get_phone()
        profile.interests = self.get_interests()
        profile.save()
