from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('blog/<int:pk>/', views.blog_details, name='blog_details'),
    path('type/<str:type_name>/', views.blog_by_type, name='blog_by_type'),
    path('create/', views.create_blog, name='create_blog'),
]