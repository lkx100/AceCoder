from django.urls import path
from . import views

urlpatterns = [
    
    # All View Types
    path('', views.home, name='post_list'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('tag/<slug:slug>/', views.posts_by_tag, name='posts_by_tag'),
    path('pending_posts/<int:id>', views.pending_posts, name="pending_posts"),
    path('my_posts/', views.my_posts, name='my_posts'),
    
    # Additional Features
    path('like/<int:id>/', views.like_post, name="like_post"),
    
    # CRUD Operations
    path('post/create/', views.post_create, name="post_create"),
    path('post/<int:id>/delete/', views.post_delete, name="post_delete"),
    path('post/<int:id>/update/', views.post_update, name="post_update"),
]