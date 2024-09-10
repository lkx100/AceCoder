import os
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class BlogType(models.Model):
    type_name = models.CharField(max_length=20)

    def __str__(self):
        return self.type_name

def blog_file_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/blog_type/<filename>
    return f'blog/{instance.blog_type.type_name}/{filename}'

class Blogging(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)  # This will be populated from the file
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    blog_type = models.ForeignKey(BlogType, on_delete=models.CASCADE)
    file = models.FileField(upload_to=blog_file_path)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Read content from the file and save it to the content field
        if self.file:
            self.content = self.file.read().decode('utf-8')
        super().save(*args, **kwargs)