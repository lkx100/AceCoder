from django.shortcuts import render, get_object_or_404
from .models import Post, Tag, PostImage
from bs4 import BeautifulSoup

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
    soup = BeautifulSoup(str(post.get_markdown()[1]), 'html.parser')
    links = soup.select('li > a')
    href_list, text_list = [], []
    
    for link in links:
        href_list.append(link.get('href'))
        text_list.append(link.text)

    toc_items = zip(href_list, text_list)

    context = {
        'post': post,
        'toc_items': toc_items,
    }
    return render(request, 'post_detail.html', context)
