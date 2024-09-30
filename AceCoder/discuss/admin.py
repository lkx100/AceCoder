from django.contrib import admin
from .models import Comment, Category, Discussion

admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Discussion)
