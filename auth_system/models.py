from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify

from django.conf import settings


class SubscriptionManager(models.Manager):
    def follow(self, follower, following):
        if follower != following:
            self.create(follower=follower, following=following)

    def unfollow(self, follower, following):
        return self.get(follower=follower, following=following).delete()

    def is_following(self, follower, following):
        return self.filter(follower=follower, following=following).exists()

    def is_followed_by(self, follower, following):
        return self.filter(follower=following, following=follower).exists()


class User(AbstractUser):
    first_login = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=18, verbose_name='Номер телефону')
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.username} - "
    
    class Meta:
        verbose_name = 'Користувач'
        verbose_name_plural = 'Користувачі'
        ordering = ['-first_login']


class UserProfile(models.Model):
    GENDER_CHOICE = (
        ('-', '-'),
        ('male', 'чоловіча'),
        ('female', 'жіноча')
    )
    bio = models.TextField(blank=True, null=True, verbose_name='Біографія')
    avatar = models.ImageField(upload_to='user/avatar/', blank=True, null=True, verbose_name='Аватар')
    birthday = models.DateField(blank=True, null=True, verbose_name='Дата народження')
    gender = models.CharField(max_length=6, choices=GENDER_CHOICE, default='-', verbose_name='Стать')
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')

    def __str__(self):
        return f'Profile for {self.user.username}'
    
    class Meta:
        verbose_name = 'Профіль'
        verbose_name_plural = 'Профілі'

class Subscription(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = SubscriptionManager()

    class Meta:
        unique_together = ('follower', 'following')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.follower.username} following {self.following.username}'
    
    class Meta:
        verbose_name = 'Підписка'
        verbose_name_plural = 'Підписки'
        ordering = ['-created_at']


