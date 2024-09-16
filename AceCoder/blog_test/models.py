from django.db import models
from markdownfield.models import MarkdownField, RenderedMarkdownField
from markdownfield.validators import VALIDATOR_STANDARD

class BlogPage(models.Model):
    title = models.CharField(max_length=200)
    content = MarkdownField(
        rendered_field = 'text_rendered',
        validator = VALIDATOR_STANDARD,
        use_editor = True,
        use_admin_editor = True
    )
    text_rendered = RenderedMarkdownField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
