from django.db import models
from markdownfield.validators import VALIDATOR_STANDARD

class BlogPage(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title
