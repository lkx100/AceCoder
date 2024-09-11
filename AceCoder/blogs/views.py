from django.shortcuts import render, get_object_or_404
from .models import Blog, BlogTag, Content, ContentType, Section

def all_blogs(request):
    all_tags = BlogTag.objects.all()
    blogs = Blog.objects.all()
    context = {
        'all_tags': all_tags,
        'blogs': blogs,
    }
    return render(request, "all_blogs.html", context)

def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    # get all sections & content for the blog
    sections = Section.objects.filter(blog=blog).order_by('order')
    # Prepare a list to hold sections with their content
    sections_with_content = []
    
    # for section in sections:
    #     # Get all content for this section
    #     content = Content.objects.filter(section=section)
    #     sections_with_content.append({
    #         'section': section,
    #         'content': content
    #     })

    for section in sections:
        # Get all content for this section
        content = Content.objects.filter(section=section).order_by('order')
        print(f"{section.section_title}")
        content_list = []
        for item in content:
            # item --> object
            content_types = item.content_type.all()
            content_type = content_types.first().type if content_types.exists() else 'text'
            content_dict = {
                'content_type': content_type,
                'content': item.text  # Assuming there's a 'content' field
            }
            # print(f"{item.text}")
            # Handle different content types
            if content_type == 'image':
                content_dict['content'] = item.image.url if item.image else None
            elif content_type == 'code':
                content_dict['content'] = item.text  # Assuming code is stored in the text field
            
            print(f"{content_dict}")
            content_list.append(content_dict)
        
        sections_with_content.append({
            'section': section,
            'content': content_list
        })

    context = {
        'blog': blog,
        'sections_with_content': sections_with_content,
    }
    # print(blog)
    # print(sections_with_content)
    return render(request, "blog_detail.html", context)

def tag_page(request, tag):
    tag_object = get_object_or_404(BlogTag, tag=tag)
    all_blogs_for_tag = Blog.objects.filter(blog_tag=tag_object)
    all_tags = BlogTag.objects.all()
    context = {
        'all_blogs': all_blogs_for_tag,
        'all_tags': all_tags,
        'tag': tag,
    }
    return render(request, "tag_page.html", context)