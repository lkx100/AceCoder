from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.http import HttpResponse
from .models import *
from .Codechef import CodechefTools
import pandas as pd
from django.contrib import messages
from django.conf import settings
from .decorators import *

# Create your views here.
def home(request):

    if request.user.is_authenticated:
        email = request.user.email
        email_domain = email.split('@')[1] if '@' in email else ''
        allowed_domains = settings.ALLOWED_EMAILS
        
        if email_domain not in allowed_domains and not request.user.is_superuser:
            messages.warning(request, "Given email is not example@klh.edu.in! You have been logged out.")
            request.user.delete()
            logout(request)

            return redirect('account_login')
        
    is_admin = request.user.groups.filter(name='admin').exists()
    details = Codechef_database.objects.all().order_by('-latest_rating', 'latest_rank')
    return render(request, "home.html", {'details': details, 'is_admin': is_admin})



@isadmindashboard
def dashboard(request):
    details = Codechef_database.objects.all().order_by('student__roll_no')

    if request.method == "POST":
        download = request.POST.get('download', "False")
        plag = request.POST.get('plagarised', 'All')
        depart = request.POST.get('department', 'All')
        sortby = request.POST.get('sorting', 'None')

        if details and depart != 'All':
            details = details.filter(student__department=depart)

        if details and plag != 'All':
            details = [student for student in details if (plag == 'Yes' and student.plagarisms != 0) or (plag == 'No' and student.plagarisms == 0)]

        if details and sortby != 'None':
            if sortby == 'RatingInc':
                details = details.order_by('latest_rating')
            elif sortby == 'RatingDec':
                details = details.order_by('-latest_rating')
            elif sortby == 'RankInc':
                details = details.order_by('latest_rank')
            elif sortby == 'RankDec':
                details = details.order_by('-latest_rank')

        if download != 'False':
            return download_details_all(details)
    else:
        plag = 'All'
        sortby = 'None'
        depart = 'All'

    # print("details:" , details)

    return render(request, "dashboard.html", {"details": details, "plag": plag, "sortby": sortby, "depart": depart})

def fetch_details(request, codechef_id):
    student = CodechefTools(codechef_id)
    if student.account_exists():
        all_contests = student.feth_details()
        contests = all_contests[:]
        num_of_contests = student.fetch_num_of_contests()
        num_of_problems = student.fetch_num_of_problems()
        num_of_plagarisms = student.fetch_num_of_plagarisms()
        stars = student.stars()
        contest_problems = student.fetch_contest_problems()

        # Add problems solved to each contest
        for contest in contests:
            try:
                contest['problems_solved'] = ", ".join(contest_problems.get(contest['name'], 0))
                contest['count_problems_solved'] = len(contest_problems.get(contest['name'], 0))
            except:
                contest['problems_solved'] = None
                contest['count_problems_solved'] = None

    else:
        all_contests = None
        contests = None
        num_of_contests = None
        num_of_problems = None
        num_of_plagarisms = None
        stars = None
        contest_problems = None

    if request.method == "POST":
        download = request.POST.get('download', "False")
        plag = request.POST.get('plagarised', 'All')
        sortby = request.POST.get('sorting', 'None')

        if contests and plag!='All':
            contests = [contest for contest in contests if (plag == 'Yes' and contest['penalised_in'] is not None) or (plag == 'No' and contest['penalised_in'] is None)]

        if contests and sortby!='None':
            if sortby == 'RatingInc':
                contests.sort(key=lambda x: int(x['rating']))
            elif sortby == 'RatingDec':
                contests.sort(key=lambda x: int(x['rating']), reverse=True)
            elif sortby == 'RankInc':
                contests.sort(key=lambda x: int(x['rank']))
            elif sortby == 'RankDec':
                contests.sort(key=lambda x: int(x['rank']), reverse=True)

        details = {
            "codechef_id": codechef_id,
            "contests": contests,
            "num_of_contests": num_of_contests,
            "num_of_plagarisms": num_of_plagarisms,
            "num_of_problems": num_of_problems,
            "stars": stars,
            "all_contests": all_contests,
            "plag": plag,
            "sortby": sortby,
        }

        if download != 'False':
            return download_details(details)
    else:
        plag = 'All'
        sortby = 'None'
        details = {
            "codechef_id": codechef_id,
            "contests": contests,
            "num_of_contests": num_of_contests,
            "num_of_plagarisms": num_of_plagarisms,
            "num_of_problems": num_of_problems,
            "stars": stars,
            "all_contests": all_contests,
            "plag": plag,
            "sortby": sortby,
        }

    return render(request, "fetch_details.html", {'details': details})

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

def download_details_all(details):
    print("Function called!")
    rows = []

    for student in details:
        row = {
            'Roll No': student.student.roll_no,
            'Name': student.student.name,
            'Year': student.student.year,
            'Department': student.student.department,
            'Last Contest': student.last_contest,
            'Latest Rating': student.latest_rating,
            'Latest Rank': student.latest_rank,
            'Plagiarisms': student.plagarisms,
            'Contest Problems Solved': student.contest_problems,
        }

        rows.append(row)

    details_df = pd.DataFrame(rows)
    print(details_df)

    # Create a response object
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Codechef_contest_details.csv"'

    details_df.to_csv(response, index=False)

    return response