from .models import Comment, Post
from django import forms
from ckeditor.fields import RichTextField


class PostForm(forms.ModelForm):

    content = RichTextField()
    class Meta:
        model = Post
        fields = ['content']


class CommentForm(forms.ModelForm):  # 文章评论表单

    class Meta:
        model = Comment
        fields = ['body']
