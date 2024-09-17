from django import forms
from .models import BlogPage

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPage
        fields = ['title']

        