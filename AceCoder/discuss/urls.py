from django.urls import path
from . import views

urlpatterns = [
    path('', views.discussion_home, name='discussion_home'),
    path('new/', views.create_discussion, name='create_discussion'),
    path('category/<slug:slug>/', views.categorys_by_name, name='categorys_by_name'),
    path('<slug:slug_title>/', views.discussion_detail, name='discussion_detail'),
]
