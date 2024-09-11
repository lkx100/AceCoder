from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Blogging, BlogType
import markdown2

def blog_list(request):
    blogs = Blogging.objects.all().order_by('-created_at')
    return render(request, 'blog_list.html', {'blogs': blogs})

def blog_details(request, pk):
    blog = get_object_or_404(Blogging, pk=pk)
    html_content = markdown2.markdown(blog.content)
    return render(request, 'blog_details.html', {
        'blog': blog,
        'html_content': html_content
    })

def blog_by_type(request, type_name):
    blog_type = get_object_or_404(BlogType, type_name=type_name)
    blogs = Blogging.objects.filter(blog_type=blog_type).order_by('-created_at')
    return render(request, 'blog_list.html', {
        'blogs': blogs,
        'type': blog_type
    })

@login_required
def create_blog(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        blog_type_id = request.POST.get('blog_type')
        file = request.FILES.get('file')
        
        if title and blog_type_id and file:
            blog_type = get_object_or_404(BlogType, id=blog_type_id)
            blog = Blogging.objects.create(
                title=title,
                blog_type=blog_type,
                author=request.user,
                file=file
            )
            return redirect('blog_detail', pk=blog.pk)
    
    blog_types = BlogType.objects.all()
    return render(request, 'create_blog.html', {'blog_types': blog_types})