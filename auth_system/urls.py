from django.urls import path
from auth_system import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login_view, name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('registration/', views.UserRegistrationView.as_view(), name='registration'),
    path('edit_profile/<int:pk>', views.edit_profile_view, name='edit-profile'),
    path('profile/<int:pk>', views.info_profile_view, name='info-profile'),
    path('profiles/', views.profiles_list_view, name='profiles-list'),
    path('followed_profiles/', views.followed_profiles_list_view, name='followed-profiles_list'),
    path('profile/<int:pk>/follow', views.follow_unfollow_profile_view, name='follow-profile')
]
