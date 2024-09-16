from django.db import models
from django.conf import settings


class Post(models.Model):
    text = models.TextField(max_length=1024)
    image = models.ImageField(upload_to='posts', blank=True, null=True)
    views = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_post', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'Post #{self.pk} by {self.user.username}'

    def total_likes(self):
        return self.likes.count()

    def user_is_liked(self, user):
        return self.likes.filter(username=user)

    class Meta:
        ordering = ['-updated_at']


class PostView(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    text = models.TextField(max_length=1024)
    image = models.ImageField(upload_to='comments', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'Comment by {self.author.username} for {self.post.pk} post'

