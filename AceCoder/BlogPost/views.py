from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Tag, PostImage
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from .models import Tag
from .forms import PostForm

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

def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    
    return render(request, 'post_delete.html', {'post': post})

def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('post_list')
        # post = request.POST
        # post_banner = request.FILES.get('banner')
        # title = post.get('title')
        # description = post.get('description')
        # content = post.get('content')
        # tags = post.getlist('tags')
        # author = post.get('author')
        # Post.objects.create(
        #     title=title, description=description, content=content, banner=post_banner, 
        #     author=author, tags=tags
        # )
    else:
        form = PostForm()
    # users = User.objects.all()
    # tags = Tag.objects.all()
    context = {
        # 'users': users,
        # 'tags': tags,
        'form': form,
    }
    return render(request, 'post_create.html', context)

def post_update(request, id):
    post = Post.objects.get(id=id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)

    context = {
        'post': post,
        'form': form,
    }
    return render(request, 'post_update.html', context)

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
