from django.urls import path
from . import views

urlpatterns = [
    path("", views.all_blogs, name="all_blogs"),
    path("<int:blog_id>/", views.blog_detail, name="blog_detail"),
    path("<str:tag>/", views.tag_page, name="tag_page"),
]
