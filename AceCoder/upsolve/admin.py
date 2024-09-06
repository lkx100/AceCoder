from django.contrib import admin
from .models import ContestProblem, Contest

class ContestAdmin(admin.ModelAdmin):
    list_display = ('name', 'contest', 'date')
    filter_horizontal = ('contest_problems',)


class ContestProblemAdmin(admin.ModelAdmin):
    list_display = ('name', 'successful_submissions', 'accuracy')



admin.site.register(Contest, ContestAdmin)
admin.site.register(ContestProblem, ContestProblemAdmin)