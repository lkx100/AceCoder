from django.contrib import admin
from .models import Tag, Post, PostImage
from markdownx.admin import MarkdownxModelAdmin

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ['name']

# Register Post model with Markdownx support
@admin.register(Post)
class PostAdmin(MarkdownxModelAdmin):
    list_display = ['title', 'author', 'created_on', 'status']
    list_filter = ['tags', 'created_on']
    search_fields = ['title', 'content']
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ['author']
    autocomplete_fields = ['tags']
    readonly_fields = ['created_on']

class PostImageAdmin(admin.ModelAdmin):
    list_display = ['slug', 'post']
admin.site.register(PostImage, PostImageAdmin)
