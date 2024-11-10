from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views.generic import CreateView

from auth_system import forms
from auth_system import models
from auth_system.decorators import user_is_owner_required


@login_required
def index(request):
    # if request.method == 'GET':
    return render(request, 'auth_system/index.html')


def user_login_view(request):
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('index')
                else:
                    return HttpResponse("Користувача відключено!")
            else:
                return HttpResponse("Неправильний логін або пароль!")
    else:
        form = forms.LoginForm()
    return render(request, 'auth_system/login.html', {'form': form})


# class CustomLoginView(LoginView):
#     template_name = 'auth_system/login.html'
#     redirect_authenticated_user = True


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
@user_is_owner_required(lambda pk: get_object_or_404(models.UserProfile, id=pk))
def edit_profile_view(request, pk):
    if request.method == 'POST':
        user_form = forms.UserEditForm(instance=request.user, data=request.POST)
        profile_form = forms.ProfileEditForm(instance=request.user.userprofile, data=request.POST, files=request.FILES)
        if user_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('info-profile', pk=pk)
    else:
        user_form = forms.UserEditForm(instance=request.user)
        profile_form = forms.ProfileEditForm(instance=request.user.userprofile)
        return render(request, 'auth_system/edit.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def info_profile_view(request, pk):
    if request.method == 'GET':
        profile = models.UserProfile.objects.get(id=pk)
        user = models.UserProfile.objects.get(id=request.user.userprofile.pk)
        is_follow = models.Subscription.objects.is_following(follower=user, following=profile)
        return render(request, 'auth_system/profile_info.html', {'profile': profile, 'is_follow': is_follow})


@login_required
def profiles_list_view(request):
    if request.method == 'GET':
        # profiles = models.UserProfile.objects.all()
        profiles = models.UserProfile.objects.exclude(id=request.user.userprofile.pk)
        return render(request, 'auth_system/profiles_list.html', {'profiles': profiles})


@login_required
def followed_profiles_list_view(request):
    if request.method == 'GET':
        # profiles = models.UserProfile.objects.filter(followers__follower=request.user.pk)
        subscriptions = models.Subscription.objects.filter(follower=request.user.userprofile.pk).select_related('following')
        profiles = [subscription.following for subscription in subscriptions]
        return render(request, 'auth_system/followed_profiles_list.html', {'profiles': profiles})


@login_required
def follow_unfollow_profile_view(request, pk):
    if request.method == 'GET':
        follower = models.UserProfile.objects.get(id=request.user.userprofile.pk)
        following = models.UserProfile.objects.get(id=pk)
        if models.Subscription.objects.is_following(follower, following):
            models.Subscription.objects.unfollow(follower, following)
        else:
            models.Subscription.objects.follow(follower, following)
            print('follow')
        return redirect('info-profile', pk=pk)









