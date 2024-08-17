from django.shortcuts import render
from .models import Post

def resources_home(request):
    blogs = Post.objects.all()
    return render(request, 'resources_home.html', context = {'blogs': blogs})

def blog_page(request, blog_id):
    blog = Post.objects.all()[blog_id-1]
    return render(request, 'blog_page.html', context = {'blog': blog})
