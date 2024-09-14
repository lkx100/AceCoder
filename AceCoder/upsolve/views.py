from django.shortcuts import render, get_object_or_404
from .models import Contest, ContestProblem, Tag

def upsolve_home(request):
    contests = Contest.objects.all().order_by('-date')
    return render(request, 'past_contests.html', {'contests': contests})

def contest_page(request, contest_name):
    contest = get_object_or_404(Contest, name=contest_name)
    solution_link = contest.solution_link
    problems = contest.contest_problems.all()
    context = {
        'contest_name': contest_name, 
        'problems': problems,
        'solution_link': solution_link
    }
    return render(request, 'contest_page.html', context)

def problem_set(request):
    problems = list(ContestProblem.objects.all())
    context = {
        'problems': problems,
    }
    for problem in problems:
        problem.problem_tags_str = ", ".join([tag.tag for tag in problem.problem_tags.all()])
        
    return render(request, 'problem_set.html', context)
