from django.shortcuts import render
from .models import *

# Create your views here.
def home(request):

    details = Codechef_database.objects.all().order_by('-latest_rating', 'latest_rank')
    return render(request, "home.html", {'details': details})


def dashboard(request):

    return render(request, "dashboard.html")