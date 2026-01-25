from django import forms
from django.contrib.auth.forms import UserCreationForm

from auth_system import models


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    remember_me = forms.BooleanField(required=False)


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
            'email',
            'first_name',
            'last_name',
            'phone_number'
        )

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'phone_number': 'Номер телефону',
            'first_name': 'Ім\'я',
            'last_name': 'Прізвище',          
        }


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
            'bio': forms.TextInput(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
            'birthday': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
        }

        labels = {
            'bio': 'Біографія',
            'avatar': 'Аватар',
            'birthday': 'Дата народження',
            'gender': 'Стать',   
        }