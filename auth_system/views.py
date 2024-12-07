from allauth.account.signals import user_logged_in
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.contrib import messages
from django.dispatch import receiver
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views.generic import CreateView

from auth_system import forms
from auth_system import models
from auth_system.decorators import user_is_owner_required


def user_login_view(request):
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if not cd['remember_me']:
                        request.session.set_expiry(0)
                    return redirect('all-posts')
                else:
                    return HttpResponse("Користувача відключено!")
            else:
                return HttpResponse("Неправильний логін або пароль!")
    else:
        form = forms.LoginForm()
    return render(request, 'auth_system/login.html', {'form': form})


@receiver(user_logged_in)
def on_user_login(sender, request, user, **kwargs):
    try:
        social_account = SocialAccount.objects.get(user=user, provider='google')
        extra_data = social_account.extra_data
        profile = models.UserProfile.objects.create(user=social_account.user)
        # avatar = social_account.extra_data.get('picture', '')
        # if avatar:
        #     profile.avatar = avatar
        profile.save()
    except SocialAccount.DoesNotExist:
        pass


class CustomLogoutView(LogoutView):
    next_page = 'login'


class UserRegistrationView(CreateView):
    template_name = 'auth_system/registration.html'
    form_class = forms.UserRegistrationForm
    model = models.User
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        user.set_password(form.cleaned_data['password'])
        user.save()
        models.UserProfile.objects.create(user=user)
        # login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form):
        return redirect('registration')


@login_required
@user_is_owner_required(lambda slug: get_object_or_404(models.User, slug=slug))
def edit_profile_view(request, slug):
    if request.method == 'POST':
        user_form = forms.UserEditForm(instance=request.user, data=request.POST)
        profile_form = forms.ProfileEditForm(instance=request.user.userprofile, data=request.POST, files=request.FILES)
        if user_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user-info', slug=slug)
    else:
        user_form = forms.UserEditForm(instance=request.user)
        profile_form = forms.ProfileEditForm(instance=request.user.userprofile)
        return render(request, 'auth_system/edit.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def info_profile_view(request, slug):
    if request.method == 'GET':
        user_info = models.User.objects.get(slug=slug)
        request_user = models.User.objects.get(slug=request.user.slug)
        is_follow = models.Subscription.objects.is_following(follower=request_user, following=user_info)
        return render(request, 'auth_system/profile_info.html', {'user': user_info, 'is_follow': is_follow})


@login_required
def profiles_list_view(request):
    if request.method == 'GET':
        # profiles = models.UserProfile.objects.all()
        users = models.User.objects.exclude(slug=request.user.slug)
        return render(request, 'auth_system/profiles_list.html', {'users': users})


@login_required
def followed_profiles_list_view(request):
    if request.method == 'GET':
        # profiles = models.UserProfile.objects.filter(followers__follower=request.user.pk)
        subscriptions = models.Subscription.objects.filter(follower=request.user).select_related('following')
        users = [subscription.following for subscription in subscriptions]
        return render(request, 'auth_system/followed_profiles_list.html', {'users': users})


@login_required
def follow_unfollow_profile_view(request, slug):
    if request.method == 'GET':
        follower = models.User.objects.get(slug=request.user.slug)
        following = models.User.objects.get(slug=slug)
        if models.Subscription.objects.is_following(follower, following):
            models.Subscription.objects.unfollow(follower, following)
        else:
            models.Subscription.objects.follow(follower, following)
        return redirect('user-info', slug=slug)









