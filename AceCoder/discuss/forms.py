from django_ckeditor_5.widgets import CKEditor5Widget
from django import forms
from .models import Discussion, Comment, Category

class DiscussionForm(forms.ModelForm):
    class Meta:
        model = Discussion
        fields = ['title', 'content', 'category']

class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditor5Widget())
    class Meta:
        model = Comment
        fields = ['content', 'parent']  # 'parent' is used for nested replies
        
        widgets = {
            'parent': forms.HiddenInput(),  # Hidden field for replies
            # 'content': CKEditor5Widget(
            #     attrs={'class': 'form-control'},
            #     config_name='extends'
            # )
        }
