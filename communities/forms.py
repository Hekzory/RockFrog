from django import forms
from .models import *
from django.core.exceptions import ValidationError

class GroupEditForm(forms.Form):
    groupname = forms.CharField(max_length=40)
    slug = forms.SlugField(max_length=40)
    description = forms.CharField(required=False)

    def clean_groupname(self):
        new_groupname = self.cleaned_data['groupname']
        return new_groupname

    def save(self, group):
        group.groupname = self.cleaned_data['groupname']
        group.description = self.cleaned_data['description']
        group.slug = self.cleaned_data['slug']
        group.save()
        return group

class ArticleForm(forms.ModelForm):
    class Meta:    
        model = GroupArticle   
        fields = ['text'] 

        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control'}),
        }