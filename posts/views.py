from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from posts import models, forms
from auth_system.models import User
from posts.mixins import UserIsAuthorMixin


@login_required
def all_posts_view(request):
    if request.method == 'GET':
        posts = models.Post.objects.all().annotate(total_likes=Count('likes'), is_liked=Count('likes',
                                                                                              filter=Q(
                                                                                                  likes__id=request.user.pk)))
        create_post_form = forms.PostForm()
        context = {
            'posts': posts,
            'create_post_form': create_post_form,
        }
        return render(request, 'posts/posts_list.html', context)
    else:
        create_post_form = forms.PostForm(request.POST)
        if create_post_form.is_valid():
            data = create_post_form.cleaned_data
            models.Post.objects.create(
                text=data['text'],
                image=data['image'],
                user=request.user
            )
            return redirect('all-posts')
        else:
            return HttpResponse('Not valid')


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
        if not models.PostView.objects.filter(post=self.object, user=self.request.user).exists():
            models.PostView.objects.create(post=self.object, user=self.request.user)
            self.object.views += 1
            self.object.save()

        likes = self.object.total_likes()
        context.update({'likes_count': likes})
        context.update({'is_author': self.object.user == self.request.user})
        comments = self.object.comments.all()
        context.update({'comments': comments})
        return context


@login_required
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
