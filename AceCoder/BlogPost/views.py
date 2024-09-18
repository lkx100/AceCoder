from django.shortcuts import render, get_object_or_404
from .models import Post, Tag, PostImage

def home(request):
    posts = Post.objects.all()
    all_tags = Tag.objects.all()
    context = {
        'posts': posts,
        'all_tags': all_tags,
    }
    return render(request, 'post_list.html', context)

def posts_by_tag(request, slug):
    all_tags = Tag.objects.all()
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags=tag).order_by('-created_on')
    context = {
        'tag': tag,
        'posts': posts,
        'all_tags': all_tags,
    }
    return render(request, 'post_list.html', context)

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'post_detail.html', {'post': post})
