from django.shortcuts import render, get_object_or_404
from bs4 import BeautifulSoup
from .models import *

# Create your views here.
def learning_path_home(request):
    all_courses = Course.objects.all()

    context = {
        "all_courses": all_courses,
    }
    return render(request, "learning_path_home.html", context=context)

def course_home(request, slug):
    course = get_object_or_404(Course, slug=slug)
    course_chapters = Chapter.objects.filter(course=course).order_by("chapter_num")

    context = {
        "course": course,
        "course_chapters": course_chapters,
    }
    return render(request, "course.html", context=context)

def chapter_home(request, slug):
    chapter = get_object_or_404(Chapter, slug=slug)
    soup = BeautifulSoup(str(chapter.get_markdown()[1]), 'html.parser')
    links = soup.select('li > a')
    href_list, text_list = [], []
    
    for link in links:
        href_list.append(link.get('href'))
        text_list.append(link.text)

    toc_items = zip(href_list, text_list)
    
    context = {
        "chapter": chapter,
        "toc_items": toc_items,
    }

    return render(request, "chapter.html", context=context)