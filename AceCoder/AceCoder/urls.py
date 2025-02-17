"""
URL configuration for AceCoder project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("dashboard.urls")),
    path('upsolve/', include("upsolve.urls")),
    path('accounts/', include("allauth.urls")),
    path('graph/', include("graph.urls")),
    path('blogpost/', include("BlogPost.urls")),
    path('learning_path/', include("learning_path.urls")),
    path('discuss/', include("discuss.urls")),
    path('', include("users.urls")),
    path('markdownx/', include('markdownx.urls')),
    path("ckeditor5/", include('django_ckeditor_5.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
