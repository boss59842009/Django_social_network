from django.urls import path
from posts import views

urlpatterns = [
    path('posts/all/', views.AllPostsView.as_view(), name='all-posts'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post/create/', views.PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/like/', views.like_unlike_view, name='like-post'),
    path('post/<int:pk>/edit/', views.PostUpdateView.as_view(), name='edit-post')
]
