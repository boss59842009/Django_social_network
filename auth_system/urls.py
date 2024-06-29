from django.urls import path
from auth_system import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('registration/', views.UserRegistrationView.as_view(), name='registration'),
    path('edit/', views.edit, name='edit'),
]
