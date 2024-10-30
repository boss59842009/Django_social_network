from django.contrib.auth.models import AbstractUser
from django.db import models


class SubscriptionManager(models.Manager):
    def follow(self, follower, following):
        if follower != following:
            self.create(follower=follower, following=following)

    def unfollow(self, follower, following):
        return self.get(follower=follower, following=following).delete()

    def is_following(self, follower, following):
        return self.get(follower=follower, following=following).exists()

    def is_followed_by(self, follower, following):
        return self.get(follower=following, following=follower).exists()


class User(AbstractUser):
    first_login = models.DateTimeField(null=True)
    phone_number = models.CharField(max_length=18)


class UserProfile(models.Model):
    GENDER_CHOICE = (
        ('-', '-'),
        ('male', 'чоловіча'),
        ('female', 'жіноча')
    )
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='user/avatar/', blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICE, default='-')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Profile for {self.user.username}'


class Subscription(models.Model):
    follower = models.ForeignKey(UserProfile, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(UserProfile, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = SubscriptionManager()

    class Meta:
        unique_together = ('follower', 'following')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.follower.username} following {self.following.username}'


