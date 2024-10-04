from django.contrib import admin
from .models import Contest, Tag, Problem

class TagAdmin(admin.ModelAdmin):
    list_display = ('tag',)


class ProblemAdmin(admin.ModelAdmin):
    list_display = ('name', 'contest', 'get_tags', 'rating')
    filter_horizontal = ('problem_tags',)

    def get_tags(self, obj):
        return ", ".join([problem.tag for problem in obj.problem_tags.all()])
    
    get_tags.short_description = 'Problem Tags'

class ContestAdmin(admin.ModelAdmin):
    list_display = ('name', 'date')

admin.site.register(Tag, TagAdmin)
admin.site.register(Contest, ContestAdmin)
admin.site.register(Problem, ProblemAdmin)