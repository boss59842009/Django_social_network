from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views.generic import CreateView

from auth_system import forms
from auth_system import models


@login_required
def index(request):
    # if request.method == 'GET':
    return render(request, 'auth_system/index.html')


def user_login(request):
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
        profile = models.UserProfile.objects.create(user=user)
        # login(self.request, user)
        return super().form_valid(form)


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = forms.UserEditForm(instance=request.user, data=request.POST)
        profile_form = forms.ProfileEditForm(instance=request.user.userprofile, data=request.POST, files=request.FILES)
        if user_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('index')
    else:
        user_form = forms.UserEditForm(instance=request.user)
        profile_form = forms.ProfileEditForm(instance=request.user.userprofile)
        return render(request, 'auth_system/edit.html', {'user_form': user_form, 'profile_form': profile_form})
