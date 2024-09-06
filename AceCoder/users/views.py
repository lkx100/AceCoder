from django.shortcuts import render, redirect
from django.contrib.auth import logout

# Create your views here.
def home(request):
    return(request, "home.html")

def logout_view(request):
    logout(request)
    return redirect("/")

def invalid_email(request):
    return render(request, 'invalid_email.html')