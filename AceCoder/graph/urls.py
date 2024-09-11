from django.urls import path
from . import views

urlpatterns = [
    path("", views.graph_home, name = "graph"),   # graph/
    path("student/<str:codechef_id>/", views.graph_student, name = "graphofstudent"),   # graph/
]