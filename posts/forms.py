from django import forms
from posts import models


class PostForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ['text', 'image']

        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control form-label', 'cols': 80, 'rows': 5}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['text', 'image']


