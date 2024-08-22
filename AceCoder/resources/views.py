from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Post, PostTag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def resources_home(request):
    blogs = Post.objects.all()
    return render(request, 'resources_home.html', context = {'blogs': blogs})

def blog_page(request, blog_id):
    # blog = Post.objects.all()[blog_id-1]    # Object by indexing
    blog = get_object_or_404(Post, pk = blog_id)   # Object by id
    return render(request, 'blog_page.html', context = {'blog': blog})

# def tag_page(request, tag_id):
#     # tag_post = Post.objects.all().filter('tag' == tag_id)
#     tag_post = get_list_or_404(Post)
#     return render(request, 'tag_post.html', {'tag_post': tag_post})

def tag_posts(request, tag):
    # allPost = Post.objects.all().filter(tags__post_tag = tag)
    tag_obj = get_object_or_404(PostTag, post_tag=tag)
    allPost = Post.objects.filter(tags = tag_obj)
    return render(request, 'tag_post.html', {"tag": tag, "blogs": allPost})