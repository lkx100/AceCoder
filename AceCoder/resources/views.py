from django.shortcuts import render, get_object_or_404
from .models import Post, PostTag, SubPost

def resources_home(request):
    blogs = Post.objects.all()
    all_tags = PostTag.objects.all()
    return render(request, 'resources_home.html', context = {'blogs': blogs, 'all_tags': all_tags})

def blog_page(request, blog_id):
    blog = get_object_or_404(Post, pk = blog_id)
    all_tags = PostTag.objects.all()
    subposts = SubPost.objects.filter(parent_post = blog)
    context = {
        'blog': blog,  
        'all_tags': all_tags,
        'subposts': subposts
    }
    return render(request, 'blog_page.html', context)

def tag_posts(request, tag):
    all_tags = PostTag.objects.all()
    tag_obj = get_object_or_404(PostTag, post_tag=tag)
    blogs = Post.objects.filter(tags = tag_obj)
    return render(request, 'tag_post.html', {"tag": tag, "blogs": blogs, "all_tags": all_tags})