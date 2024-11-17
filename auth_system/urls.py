from django.urls import path
from auth_system import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login_view, name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('registration_user/', views.UserRegistrationView.as_view(), name='registration'),
    path('edit_user/<slug:slug>', views.edit_profile_view, name='user-edit'),
    path('user/<slug:slug>', views.info_profile_view, name='user-info'),
    path('all_users/', views.profiles_list_view, name='users-list'),
    path('followed_users/', views.followed_profiles_list_view, name='followed-users-list'),
    path('user/<slug:slug>/follow', views.follow_unfollow_profile_view, name='follow-user')
]
