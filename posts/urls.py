from django.urls import path
from posts import views

urlpatterns = [
    path('', views.all_posts_view, name='all-posts'),
    path('posts/all/', views.all_posts_view, name='all-posts'),
    path('post/<int:pk>/', views.post_detail_view, name='post-detail'),
    path('post/<int:pk>/like/', views.like_unlike_view, name='like-post'),
    path('post/<int:pk>/edit/', views.PostUpdateView.as_view(), name='edit-post'),
    path('post/<int:pk>/delete/', views.post_delete_view, name='delete-post')
]
