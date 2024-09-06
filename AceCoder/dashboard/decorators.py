from django.shortcuts import redirect
from django.contrib import messages
from .models import Student

def isadmindashboard(view_func):
    def _wrapped_view(request, *args, **kwargs):

        if not request.user.is_authenticated:
            messages.info(request, "Login to access Dashboard.")
            return redirect("home")

        is_admin = request.user.groups.filter(name='admin').exists()
        if not is_admin:
            roll_no = request.user.email[0:10]
            try:
                student = Student.objects.get(roll_no=roll_no)
                codechef_id = student.codechef_id
                return redirect(f"fetch_details/{codechef_id}")
            except Student.DoesNotExist:
                messages.error(request, "Student with the given roll number does not exist.")
                return redirect("home")
        return view_func(request, *args, **kwargs)
    return _wrapped_view    