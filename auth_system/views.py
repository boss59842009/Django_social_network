from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy

from auth_system import forms


# def user_login(request):
#     if request.method == 'POST':
#         form = forms.LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(username=cd['username'], password=cd['password'])
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return redirect('index')
#                 else:
#                     return HttpResponse("Користувача відключено!")
#             else:
#                 return HttpResponse("Неправильний логін або пароль!")
#     else:
#         form = forms.LoginForm()
#     return render(request, 'auth_system/login.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'auth_system/login.html'
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    next_page = 'login'


def index(request):
    # if request.method == 'GET':
    return render(request, 'auth_system/index.html')
