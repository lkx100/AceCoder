# AceCoder/context_processors.py
from django.contrib.auth.models import Group

def add_is_admin(request):
    is_admin = False
    is_faculty = False
    if request.user.is_authenticated:
        is_admin = request.user.groups.filter(name='admin').exists()
        is_faculty = request.user.groups.filter(name='Faculty').exists()
    return {'is_admin': is_admin, 'is_faculty': is_faculty}