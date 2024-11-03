from django.urls import path
from auth_system import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('registration/', views.UserRegistrationView.as_view(), name='registration'),
    path('edit_profile/<int:pk>', views.edit_profile, name='edit-profile'),
    path('profile/<int:pk>', views.info_profile, name='info-profile'),
    path('profiles/', views.profiles_list, name='profiles-list'),
    path('followed_profiles/', views.followed_profiles_list, name='followed-profiles_list'),
    path('profile/<int:pk>/follow', views.follow_unfollow_profile, name='follow-profile')
]
