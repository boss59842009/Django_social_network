from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from posts import models, forms
from auth_system.models import User, Subscription
from posts.mixins import UserIsAuthorMixin

@login_required
def all_posts_view(request):
    if request.method == 'GET':
        following_users = Subscription.objects.filter(follower=request.user).values_list('following', flat=True)
        posts = (
            models.Post.objects.filter(Q(author__in=following_users) | Q(author=request.user)).annotate(total_likes=Count('likes'),
                is_liked=Count('likes', filter=Q(likes__id=request.user.pk))
            )
        )
        posts = posts.order_by('-updated_at')
        create_post_form = forms.PostForm()
        context = {
            'posts': posts,
            'create_post_form': create_post_form,
        }
        return render(request, 'posts/posts_list.html', context)
    else:
        create_post_form = forms.PostForm(request.POST, request.FILES)
        if create_post_form.is_valid():
            data = create_post_form.cleaned_data
            models.Post.objects.create(
                text=data['text'],
                image=data['image'],
                author=request.user
            )
            return redirect('all-posts')
        else:
            return HttpResponse('Not valid')


@login_required
def post_delete_view(request, pk):
    post = models.Post.objects.get(id=pk)
    if request.user.username != post.author.username:
        return redirect('post-detail', pk=pk)

    if request.method == 'POST':
        post.delete()
        return redirect('all-posts')

    return render(request, 'posts/post_confirm_delete.html', {'post': post})


def post_detail_view(request, pk):
    if request.method == 'GET':
        post = models.Post.objects.get(id=pk)
        context = {'post': post}
        if post.user_is_liked(request.user):
            context.update({'is_liked': True})
        else:
            context.update({'is_liked': False})
        if not models.PostView.objects.filter(post=post, user=request.user).exists():
            models.PostView.objects.create(post=post, user=request.user)
            post.views += 1
            post.save()

        likes = post.total_likes()
        context.update({'likes_count': likes})
        context.update({'is_author': post.author == request.user})

        create_comment_form = forms.CommentForm()
        context.update({'create_comment_form': create_comment_form})
        comments = post.comments.all()
        context.update({'comments': comments})
        return render(request, template_name='posts/post_detail.html', context=context)
    else:
        created_post = forms.CommentForm(request.POST, request.FILES)
        if created_post.is_valid():
            data = created_post.cleaned_data
            models.Comment.objects.create(
                text=data['text'],
                image=data['image'],
                post=models.Post.objects.get(id=pk),
                author=request.user
            )
            return redirect('post-detail', pk=pk)


@login_required
def like_unlike_view(request, pk):
    if request.method == 'GET':
        post = models.Post.objects.get(id=pk)
        user = User.objects.get(username=request.user.username)
        if post.user_is_liked(user):
            post.likes.remove(user)
        else:
            post.likes.add(user)
        return redirect('post-detail', pk=pk)
    else:
        return redirect('all-posts')


class PostUpdateView(UserIsAuthorMixin, LoginRequiredMixin, UpdateView):
    model = models.Post
    form_class = forms.PostForm
    template_name = 'posts/post_edit_form.html'

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.updated_at = timezone.now()
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
