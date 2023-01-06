from .models import Comment, Post
from django import forms
from ckeditor.fields import RichTextField


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'desc', 'content', 'category']

    class Media:
        css = {
            'all': ('ckeditor5/cked.css',)
        }

        js = (
            'https://cdn.bootcdn.net/ajax/libs/jquery/3.6.0/jquery.js',
            'ckeditor5/ckeditor.js',
            'ckeditor5/translations/zh.js',
            # 'ckeditor5/config.js'
        )


class CommentForm(forms.ModelForm):  # 文章评论表单

    class Meta:
        model = Comment
        fields = ['body']
