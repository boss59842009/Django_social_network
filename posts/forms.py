from django import forms
from posts import models


class PostForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ['text', 'image']


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['text', 'image']


