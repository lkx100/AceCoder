from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='post_list'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('tag/<slug:slug>/', views.posts_by_tag, name='posts_by_tag'),
]