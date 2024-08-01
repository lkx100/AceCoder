from django.urls import path
from . import views

urlpatterns = [
    path('', views.resources_home, name="resources_home"),   # resources/
]