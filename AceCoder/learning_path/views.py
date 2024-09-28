from django.shortcuts import render, get_object_or_404
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
    course_chapters = Chapter.objects.filter(course=course)

    context = {
        "course": course,
        "course_chapters": course_chapters,
    }
    return render(request, "course.html", context=context)