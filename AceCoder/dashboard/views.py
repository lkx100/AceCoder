from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .Codechef import CodechefTools
import pandas as pd
from django.core.paginator import Paginator

# Create your views here.
def home(request):

    details = Codechef_database.objects.all().order_by('-latest_rating', 'latest_rank')
    return render(request, "home.html", {'details': details})


def dashboard(request):
    details = Codechef_database.objects.all().order_by('-latest_rating', 'latest_rank')

    return render(request, "dashboard.html", {"details": details})


def fetch_details(request, codechef_id):
    student = CodechefTools(codechef_id)
    if student.account_exists():
        all_contests = student.feth_details()
        paginator = Paginator(all_contests, 14)  # Show 15 contests per page

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        num_of_contests = student.fetch_num_of_contests()
        num_of_problems = student.fetch_num_of_problems()
        num_of_plagarisms = student.fetch_num_of_plagarisms()
        stars = student.stars()
        contest_problems = student.fetch_contest_problems()

        # Add problems solved to each contest
        for contest in page_obj:
            try:
                contest['problems_solved'] = ", ".join(contest_problems.get(contest['name'], 0))
                contest['count_problems_solved'] = len(contest_problems.get(contest['name'], 0))
            except:
                contest['problems_solved'] = None

        context = {
            'details': {
                'codechef_id': codechef_id,
                'num_of_contests': num_of_contests,
                'num_of_problems': num_of_problems,
                'num_of_plagarisms': num_of_plagarisms,
                'stars': stars,
                'contests': page_obj,
                'plag': request.POST.get('plagarised', 'All'),
                'sortby': request.POST.get('sorting', 'None')
            }
        }

        return render(request, "fetch_details.html", context)

def download_details(details):
    # Create the contests DataFrame
    contests = details['contests']
    contest_rows = []
    for contest in contests:
        row = {
            'Contest': contest['name'],
            'Rating': contest['rating'],
            'Rank': contest['rank'],
            'Plagarised': 'Yes' if contest['penalised_in'] else 'No',
            "Problems Solved": contest['count_problems_solved'],
            "Problems Solved List": contest['problems_solved'],
        }
        contest_rows.append(row)
    contests_df = pd.DataFrame(contest_rows)

    # Create the general details DataFrame
    general_details = {
        'Codechef ID': [details['codechef_id']],
        'Number of Contests': [details['num_of_contests']],
        'Number of Plagarisms': [details['num_of_plagarisms']],
        'Number of Problems Solved': [details['num_of_problems']],
        'Stars': [details['stars']]
    }
    general_details_df = pd.DataFrame(general_details)

    # Create a response object
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{details["codechef_id"]}_contest_details.csv"'

    # Write both DataFrames to the CSV file
    general_details_df.to_csv(response, index=False)
    response.write("\n\n")  # Add some space between the two tables
    contests_df.to_csv(response, index=False)

    return response