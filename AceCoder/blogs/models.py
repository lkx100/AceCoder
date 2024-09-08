from django.db import models
from django.contrib.auth.models import User

class BlogTag(models.Model):
    tag = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.tag

class Blog(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    blog_tag = models.ManyToManyField(BlogTag)
    banner = models.ImageField(upload_to = 'blogs_banner/', blank = True, null = True)
    description = models.TextField()
    created_on = models.DateField(auto_now=True)
    adited_on = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.title[:30]}...." if len(self.title) > 30 else f"{self.title}"
    


class Section(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='blog')
    section_title = models.CharField(max_length=200)
    order = models.PositiveIntegerField()

    def __str__(self):
        return self.section_title
    


class ContentType(models.Model):
    type = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.type


class Content(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="section")
    content_type = models.ManyToManyField(ContentType, related_name="content_type")
    image = models.ImageField(upload_to="blogs_ContentImages/", blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    custom_typo = models.CharField(max_length=20, blank=True, null=True)
    order = models.PositiveIntegerField(null=True, blank=True)
