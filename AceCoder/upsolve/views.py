from django.shortcuts import render, get_object_or_404
from .models import Contest, Problem, Tag
from django.core.paginator import Paginator

def upsolve_home(request):
    contests = Contest.objects.all().order_by('-date')

    context = {
        'contests': contests,
    }
    
    return render(request, 'past_contests.html', context)

def contest_page(request, contest_name):
    contest = get_object_or_404(Contest, name=contest_name)
    solution_link = contest.solution_link
    problems = contest.problems.all()

    context = {
        'contest_name': contest_name, 
        'problems': problems,
        'solution_link': solution_link
    }

    return render(request, 'contest_page.html', context)

def problem_set(request):
    # all_problems = Problem.objects.all()
    pg = Paginator(Problem.objects.all(), 20)
    page = request.GET.get('page')
    problems = pg.get_page(page)
    nums = problems.paginator.num_pages * "a"

    context = {
        'problems': problems,
        'nums': nums,
    }
        
    return render(request, 'problem_set.html', context)