from django import forms

class SendPMForm(forms.Form):
    text = forms.CharField(widget=forms.TextInput, label="")
    text.widget.attrs.update({'class': 'form-control'})