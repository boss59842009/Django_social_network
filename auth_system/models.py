from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_login = models.DateTimeField(null=True)
    phone_number = models.CharField(max_length=14)


class UserProfile(models.Model):
    GENDER_CHOICE = (
        ('-', '-'),
        ('male', 'male'),
        ('female', 'female')
    )
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='static/user/avatar/', blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICE, default='-')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Profile for {self.user.username}'




