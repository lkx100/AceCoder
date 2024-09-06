from django.contrib import admin
from .models import Post, PostTag, SubPost

class PostAdmin(admin.ModelAdmin):
    list_display = ('tittle', 'display_tags', 'author' ,'created_on')
    filter_horizontal = ('tags',)

    def display_tags(self, obj):
        return ", ".join([tag.post_tag for tag in obj.tags.all()])
    display_tags.short_description = 'Tags'


class SubPostAdmin(admin.ModelAdmin):
    list_display = ('tittle', 'display_tags')
    filter_horizontal = ('parent_post',)

    def display_tags(self, obj):
        return ", ".join([post.tittle for post in obj.parent_post.all()])
    display_tags.short_description = 'Associated Blog'    


admin.site.register(Post, PostAdmin)
admin.site.register(PostTag)
admin.site.register(SubPost, SubPostAdmin)    
