# AceCoder/context_processors.py
from django.contrib.auth.models import Group

def add_is_admin(request):
    is_admin = False
    if request.user.is_authenticated:
        is_admin = request.user.groups.filter(name='admin').exists()
    return {'is_admin': is_admin}