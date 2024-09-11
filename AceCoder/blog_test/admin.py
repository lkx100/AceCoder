from django.contrib import admin
from .models import BlogType, Blogging

@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('type_name',)

@admin.register(Blogging)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'blog_type', 'created_at', 'updated_at')
    readonly_fields = ('content',)

    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        obj.save()