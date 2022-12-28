from .models import Comment
from django import forms


class CommentForm(forms.ModelForm):  # 文章评论表单
    class Meta:
        model = Comment
        fields = ['body']

    class Media:
        css = {
            'all': ('ckeditor5/cked.css',)
        }

        js = (
            'https://cdn.bootcdn.net/ajax/libs/jquery/3.6.0/jquery.js',
            'ckeditor5/ckeditor.js',
            'ckeditor5/translations/zh.js',
            'ckeditor5/config.js'
        )