from django.urls import path
from . import views

urlpatterns = [
    path("", views.upsolve_home, name="upsolve_home"),
    path("<str:contest_name>/", views.contest_page, name="contest_page")
]