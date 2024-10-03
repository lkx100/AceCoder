from django.contrib import admin
from .models import ContestProblem, Contest, Tag

class TagAdmin(admin.ModelAdmin):
    list_display = ('tag',)

class ContestAdmin(admin.ModelAdmin):
    list_display = ('name', 'contest', 'date')
    filter_horizontal = ('contest_problems',)


class ContestProblemAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_tags', 'rating')
    filter_horizontal = ('problem_tags',)

    def get_tags(self, obj):
        return ", ".join([problem.tag for problem in obj.problem_tags.all()])
    
    get_tags.short_description = 'Problem Tags'



admin.site.register(Contest, ContestAdmin)
admin.site.register(ContestProblem, ContestProblemAdmin)
admin.site.register(Tag, TagAdmin)