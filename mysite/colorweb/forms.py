from django import forms
from .models import *
import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

class ImageForm(forms.ModelForm):
    class Meta:
        model = BlackWhiteImage
        fields = ['bw_img']

class Registrationform(forms.Form):
    username = forms.CharField(label='Account', max_length=30)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Re-enter Password', widget=forms.PasswordInput())

    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2 and password1:
                return password2
        raise forms.ValidationError("Invalid Password")

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'\w+$', username):
            raise forms.ValidationError("Username has a special character.")
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError("Username already exists.")

    def save(self):
        user = User.objects.create_user(username=self.cleaned_data['username'],\
                                 email=self.cleaned_data['email'],\
                                 password=self.cleaned_data['password1'])
        return user
