from django.urls import path, include
from auth_system import views

urlpatterns = [
    path('accounts/login/', views.user_login_view, name='login'),
    path('accounts/', include('allauth.urls')),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('registration-user/', views.UserRegistrationView.as_view(), name='registration'),
    path('edit-user/<slug:slug>', views.edit_profile_view, name='user-edit'),
    path('user/<slug:slug>', views.info_profile_view, name='user-info'),
    path('all-users/', views.profiles_list_view, name='users-list'),
    path('followed-users/', views.followed_profiles_list_view, name='followed-users-list'),
    path('user/<slug:slug>/follow', views.follow_unfollow_profile_view, name='follow-user')
]
