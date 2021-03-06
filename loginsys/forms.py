from django import forms
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'col-md-12 form-control'}))
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username' : forms.TextInput(attrs={'class' : 'col-md-12 form-control'}),
            'email' : forms.TextInput(attrs={'class' : 'col-md-12 form-control'})
        }