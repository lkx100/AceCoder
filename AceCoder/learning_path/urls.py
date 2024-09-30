from django.urls import path
from . import views

urlpatterns = [
    path('', views.learning_path_home, name="learning_path"),
    path('course/<str:slug>', views.course_home, name="course"),
    path('course/chapter/<str:slug>', views.chapter_home, name="chapter")
]