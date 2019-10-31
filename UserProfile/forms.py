from django import forms
from .models import Profile
from django.core.exceptions import ValidationError

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user', 'about', 'birth_date', 'email', 'city', 'phone', 'interests']
        widgets = {
            'user' : forms.TextInput(attrs={'class' : 'form-control'}),
            'about' : forms.Textarea(attrs={'class' : 'form-control'}),
            'birth_date' : forms.DateInput(attrs={'class' : 'form-control'}),
            'email' : forms.EmailInput(attrs={'class' : 'form-control'}),
            'city' : forms.TextInput(attrs={'class' : 'form-control'}),
            'phone' : forms.NumberInput(attrs={'class' : 'form-control'}),
            'interests' : forms.Textarea(attrs={'class' : 'form-control'}),
        }
