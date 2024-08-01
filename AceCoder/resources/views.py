from django.shortcuts import render

def resources_home(request):
    return render(request, 'resources_home.html')
