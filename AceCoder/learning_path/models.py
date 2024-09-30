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

    chapter_numbers = (
        (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10),
        (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20),
    )

    name =models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.CharField(max_length = 200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    course = models.ForeignKey(Course, related_name='chapters', on_delete=models.CASCADE)  # Add this line
    chapter_num = models.IntegerField(choices=chapter_numbers, default=0)


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

        # Truncate the content to the first 100 characters
        truncated_content = content[:1000]
        truncated_html_content = md.convert(truncated_content)

        return mark_safe(html_content), mark_safe(toc), mark_safe(truncated_html_content)

    def __str__(self):
        return f"{self.name} - {self.course.name}"