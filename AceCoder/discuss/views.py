from django.shortcuts import render, get_object_or_404, redirect
from .models import Discussion, Category
from .forms import CommentForm, DiscussionForm
from django.contrib.auth.decorators import login_required

def discussion_home(request):
    discussions = Discussion.objects.all().order_by('-created_at')[:10]  # Top 10 discussions
    all_categorys = Category.objects.all()

    context = {
        'discussions': discussions,
        'all_categorys': all_categorys,
    }

    return render(request, 'discussion_list.html', context)

def categorys_by_name(request, slug):
    all_categorys = Category.objects.all()
    name = get_object_or_404(Category, slug=slug)
    discussions = Discussion.objects.all().filter(category=name)

    context = {
        'discussions': discussions,
        'name': name,
        'all_categorys': all_categorys,
    }
    return render(request, 'discussion_list.html', context)

def discussion_detail(request, slug_title):
    discussion = get_object_or_404(Discussion, slug=slug_title)
    comments = discussion.comments.filter(parent__isnull=True)  # Top-level comments
    all_categorys = Category.objects.all()
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.discussion = discussion
            comment.save()
            return redirect('discussion_detail', slug_title=discussion.slug)
    else:
        form = CommentForm()

    context = {
        'discussion': discussion,
        'comments': comments,
        'form': form,
        'all_categorys': all_categorys,
    }
    
    return render(request, 'discussion_detail.html', context)


@login_required
def create_discussion(request):
    if request.method == 'POST':
        form = DiscussionForm(request.POST)
        if form.is_valid():
            discussion = form.save(commit=False)
            discussion.user = request.user
            discussion.save()
            return redirect('discussion_detail', slug_title=discussion.slug)
    else:
        form = DiscussionForm()
    
    context = {
        'form': form
    }

    return render(request, 'create_discussion.html', context)
