from django import forms
from django.contrib.auth.forms import UserCreationForm

from auth_system import models


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Підтвердити пароль', widget=forms.PasswordInput)

    class Meta:
        model = models.User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number'
        )

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number'
        )


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = models.UserProfile
        fields = (
            'bio',
            'avatar',
            'birthday',
            'gender',
        )
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'})
        }