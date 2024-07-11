from django.urls import path
from posts import views

urlpatterns = [
    path('posts/all/', views.AllPostsView.as_view(), name='all-posts'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post/create/', views.PostCreateView.as_view(), name='post-create')
]
