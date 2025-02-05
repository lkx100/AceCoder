from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Tag, PostImage
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from .models import Tag
from .forms import PostForm
from AceCoder.context_processors import add_is_admin
from django.contrib.auth.decorators import login_required

# All View Types
def home(request):
    posts = Post.objects.all().filter(status='1').order_by('-created_on')
    all_tags = Tag.objects.all()
    
    if request.GET.get('search'):
        posts = Post.objects.filter(title__icontains = request.GET.get('search'))

    is_admin = False
    is_faculty = False
    if request.user.is_authenticated:
        is_admin = request.user.groups.filter(name='admin').exists()
        is_faculty = request.user.groups.filter(name='Faculty').exists()
    
    context = {
        'posts': posts,
        'all_tags': all_tags,
        'search_word': request.GET.get('search'),
        'is_authorised': is_admin or is_faculty,
        'is_admin': is_admin,
    }

    return render(request, 'post_list.html', context)

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    user_has_liked = post.has_user_liked(request.user)
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
        'user_has_liked': user_has_liked,
    }
    return render(request, 'post_detail.html', context)

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

def pending_posts(request, id=0):
    if id:
        post = Post.objects.get(id=id)
        post.status = '1'
        post.save()
    all_tags = Tag.objects.all()
    pending_post = Post.objects.filter(status='0')
    context = {
        'posts': pending_post,
        'all_tags': all_tags,
        'tag': 'Pending',
    }

    return render(request, 'pending_posts.html', context)

@login_required
def my_posts(request):
    posts = Post.objects.filter(author=request.user)
    all_tags = Tag.objects.all()
    context = {
        'posts': posts,
        'all_tags': all_tags,
        'is_authorised': True,
        'tag': 'My'
    }
    return render(request, 'post_list.html', context)

# Additional Features
@login_required
def like_post(request, id):
    post = get_object_or_404(Post, id=id)

    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect('post_detail', slug=post.slug)

# CRUD Operations
@login_required
def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    
    return render(request, 'post_delete.html', {'post': post})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
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

@login_required
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
