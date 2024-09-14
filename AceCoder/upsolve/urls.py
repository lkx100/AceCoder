from django.urls import path
from . import views

urlpatterns = [
    path("", views.upsolve_home, name="upsolve_home"),
    path("problem_set/", views.problem_set, name="problem_set"),
    path("<str:contest_name>/", views.contest_page, name="contest_page"),
]