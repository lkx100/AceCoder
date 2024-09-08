from django.contrib import admin
from .models import Blog, Content, Section, ContentType, BlogTag

class ContentAdmin(admin.ModelAdmin):
    filter_horizontal = ('content_type',)
    list_display = ('get_content_type', 'custom_typo', 'section')

    def get_content_type(self, obj):
        return ", ".join([type.type for type in obj.content_type.all()])   # obj.Model_name.all()
    get_content_type.short_description = 'Content Type'

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_blog_tags', 'author')

    def get_blog_tags(self, obj):
        return ", ".join([type.tag for type in obj.blog_tag.all()])
    get_blog_tags.short_description = 'Blog Tags'

class SectionAdmin(admin.ModelAdmin):
    list_display = ('section_title', 'blog')

admin.site.register(Blog, BlogAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Content, ContentAdmin)
admin.site.register(ContentType)
admin.site.register(BlogTag)
