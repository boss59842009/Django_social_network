from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from posts import models, forms
from auth_system.models import User
from posts.mixins import UserIsAuthorMixin


class AllPostsView(LoginRequiredMixin, ListView):
    model = models.Post
    template_name = 'posts/posts_list.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_post_form'] = forms.PostForm()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(total_likes=Count('likes')).order_by('-updated_at')
        return queryset


class PostDetailView(LoginRequiredMixin, DetailView):
    model = models.Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.user_is_liked(self.request.user):
            context.update({'is_liked': True})
        else:
            context.update({'is_liked': False})
            self.object.views += 1
            self.object.save()
        likes = self.object.total_likes()
        context.update({'likes_count': likes})
        context.update({'is_author': self.object.user == self.request.user})
        comments = self.object.comments.all()
        context.update({'comments': comments})
        print(context)
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = models.Post
    template_name = 'posts/post_form.html'
    form_class = forms.PostForm
    success_url = reverse_lazy('all-posts')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


def like_unlike_view(request, pk):
    if request.method == 'GET':
        post = models.Post.objects.get(id=pk)
        user = User.objects.get(username=request.user)
        if post.user_is_liked(request.user):
            post.likes.remove(user)
            return redirect('post-detail', pk=pk)
        else:
            post.likes.add(user)
            return redirect('post-detail', pk=pk)
    else:
        return redirect('all-posts')


class PostUpdateView(UserIsAuthorMixin, UpdateView):
    model = models.Post
    form_class = forms.PostForm
    template_name = 'posts/post_edit_form.html'

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_at = timezone.now()
        post.save()
        return super().form_valid(form)
        # return HttpResponse("Valid")
