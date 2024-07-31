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
        contests = student.feth_details()
        num_of_contests = student.fetch_num_of_contests()
        num_of_problems = student.fetch_num_of_problems()
        num_of_plagarisms = student.fetch_num_of_plagarisms()
        stars = student.stars()
    else:
        contests = None
        num_of_contests = None
        num_of_problems = None
        num_of_plagarisms = None
        stars = None



    details = {"codechef_id": codechef_id, "contests": contests, "num_of_contests": num_of_contests, "num_of_plagarisms": num_of_plagarisms, "num_of_problems": num_of_problems, "stars": stars}
    return render(request, "fetch_details.html", {'details': details})