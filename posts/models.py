from django.db import models
from django.conf import settings


class Post(models.Model):
    text = models.TextField(max_length=1024, verbose_name='Текст')
    image = models.ImageField(upload_to='posts', blank=True, null=True, verbose_name='Зображення')
    views = models.PositiveIntegerField(default=0, verbose_name='Перегляди')
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_post', blank=True, verbose_name='Лайки')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts', verbose_name='Автор')

    def __str__(self):
        return f'Post #{self.pk} by {self.author.username}'

    def total_likes(self):
        return self.likes.count()

    def user_is_liked(self, user):
        return self.likes.filter(username=user.username)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Пости'
        ordering = ['-updated_at']


class PostView(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_views', verbose_name='Пост')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_views', verbose_name='Користувач')
    viewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'View by {self.user.username} for {self.post.pk} post'
    
    class Meta:
        verbose_name = 'Перегляд посту'
        verbose_name_plural = 'Перегляди постів'
        ordering = ['-viewed_at']


class Comment(models.Model):
    text = models.TextField(max_length=1024, verbose_name='Текст')
    image = models.ImageField(upload_to='comments', blank=True, null=True, verbose_name='Зображення')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='Пост')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments', verbose_name='Автор')

    def __str__(self):
        return f'Comment by {self.author.username} for {self.post.pk} post'

    class Meta:
        verbose_name = 'Коментар'
        verbose_name_plural = 'Коментарі'
        ordering = ['-created_at']
