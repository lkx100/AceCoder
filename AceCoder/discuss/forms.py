from django import forms
from .models import Discussion, Comment, Category

class DiscussionForm(forms.ModelForm):
    class Meta:
        model = Discussion
        fields = ['title', 'content', 'category']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'parent']  # 'parent' is used for nested replies
        widgets = {
            'parent': forms.HiddenInput()  # Hidden field for replies
        }
