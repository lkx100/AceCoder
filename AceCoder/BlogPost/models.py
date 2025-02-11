from django.db import models
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
import markdown
from django.contrib.auth.models import User
import nbformat
import re
from nbconvert import HTMLExporter

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
    description = models.TextField()
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    banner = models.ImageField(upload_to='post_banners/', blank=True, null=True)

    # content = MarkdownxField()
    content = models.TextField(blank=True, null=True)
    ipynb = models.FileField(upload_to='notebooks/', blank=True, null=True)
    created_on = models.DateField(auto_now_add=True)

    CONTENT_TYPE_OPTION = (
        ('0', 'Markdown'),
        ('1', 'IPYNB'),
    )

    STATUS_CHOICES = (
        ('0', 'Pending'),
        ('1', 'Published'),
    )
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPE_OPTION, null=True, default='0')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, null=True, default='0')
    likes = models.ManyToManyField(User, related_name="post_likes")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.ipynb:
            self.content_type = '1'  # IPYNB
            print(f"IPYNB file: {self.ipynb}")
            try:
                print(type(self.ipynb))
                with self.ipynb.open('r') as f:
                    nb = nbformat.read(f, as_version=4)
                html_exporter = HTMLExporter()
                (body, resources) = html_exporter.from_notebook_node(nb)
                self.content = body  # Store rendered HTML in content field
            except Exception as e:
                self.content = f"Error rendering IPynb file: {e}"  # Store error message

            print(f"Content type: {self.content_type}, Content: {self.content[:100]}...")

        else:
            self.content_type = '0'  # Markdown
        super().save(*args, **kwargs)

    def total_likes(self):
        return self.likes.count()
    
    def has_user_liked(self, user):
        return self.likes.filter(id=user.id).exists()

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

