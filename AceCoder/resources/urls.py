from django.urls import path
from . import views

urlpatterns = [
    path('', views.resources_home, name = "resources_home"),   # resources/
    path('<int:blog_id>/', views.blog_page, name = "blog_page"),  # resources/3
    path('<str:tag>/', views.tag_posts, name='tag_posts'),  # resources/dsa/
]