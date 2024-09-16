from .models import BlogPage
from django.shortcuts import render, redirect
from .forms import BlogPostForm

def create_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_posts')
    else:
        form = BlogPostForm()
    
    return render(request, 'create_post.html', {'form': form})

def list_posts(request):
    posts = BlogPage.objects.all()
    return render(request, 'list_posts.html', {'posts': posts})