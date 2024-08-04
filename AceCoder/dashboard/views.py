from django.shortcuts import render
from .models import *
from .Codechef import CodechefTools

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
        contests = all_contests[:]
        num_of_contests = student.fetch_num_of_contests()
        num_of_problems = student.fetch_num_of_problems()
        num_of_plagarisms = student.fetch_num_of_plagarisms()
        stars = student.stars()
    else:
        all_contests = None
        contests = None
        num_of_contests = None
        num_of_problems = None
        num_of_plagarisms = None
        stars = None

    if request.method == "POST":
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