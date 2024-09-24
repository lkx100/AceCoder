from django.db import models
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
import markdown
from django.contrib.auth.models import User
import re

class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.CharField(max_length = 200)
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    banner = models.ImageField(upload_to='post_banners/', blank=True, null=True)

    # content = MarkdownxField()
    content = models.TextField()
    created_on = models.DateField(auto_now_add=True)

    STATUS_CHOICES = (
        ('0', 'Pending'),
        ('1', 'Published'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, null=True, default='0')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_markdown(self):

        content = self.content
        image_references = re.findall(r'\[([^\]]+)\]', content)

        for ref in image_references:
            try:
                image = self.postimage_set.get(slug = ref)
                image_markdown = f"![{image.slug}]({image.image.url})"
                content = content.replace(f"[{ref}]", image_markdown)
            except PostImage.DoesNotExist:
                pass

        md = markdown.Markdown(
            extensions=['toc', 'fenced_code']
        )

        html_content = md.convert(content)
        toc = md.toc        

        return mark_safe(html_content), mark_safe(toc)

    def __str__(self):
        return self.title


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images/')
    slug = models.CharField(max_length=100)

