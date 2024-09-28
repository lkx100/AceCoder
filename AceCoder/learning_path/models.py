from django.db import models
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
import markdown
from django.contrib.auth.models import User
import re

# Create your models here.
class Course(models.Model):
    name =models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.CharField(max_length = 200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    banner = models.ImageField(upload_to='post_banners/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Chapter(models.Model):
    name =models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.CharField(max_length = 200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    course = models.ForeignKey(Course, related_name='chapters', on_delete=models.CASCADE)  # Add this line


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_markdown(self):
        content = self.content
        image_references = re.findall(r'\[([^\]]+)\]', content)

        for ref in image_references:
            try:
                image = self.postimage_set.get(slug=ref)
                image_markdown = f"![{image.slug}]({image.image.url})"
                content = content.replace(f"[{ref}]", image_markdown)
            except:
                pass

        md = markdown.Markdown(
            extensions=['toc', 'fenced_code']
        )

        html_content = md.convert(content)
        toc = md.toc        

        return mark_safe(html_content)

    def __str__(self):
        return f"{self.name} - {self.course.name}"