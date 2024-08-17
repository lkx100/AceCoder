from django.shortcuts import render, get_object_or_404
from .models import Post

def resources_home(request):
    blogs = Post.objects.all()
    return render(request, 'resources_home.html', context = {'blogs': blogs})

def blog_page(request, blog_id):
    # blog = Post.objects.all()[blog_id-1]    # Object by indexing
    blog = get_object_or_404(Post, pk = blog_id)   # Object by id
    return render(request, 'blog_page.html', context = {'blog': blog})
