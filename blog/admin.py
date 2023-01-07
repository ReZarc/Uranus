from django.contrib import admin

# Register your models here.
from .models import Category, Post, Tag, Sidebar, Comment

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Sidebar)
admin.site.register(Comment)


class PostAdmin(admin.ModelAdmin):
    """ 文章详情管理 """

    list_display = ('id', 'title', 'category', 'tags', 'owner', 'pv', 'is_hot', 'pub_date',)
    list_filter = ('owner',)
    search_fields = ('title', 'desc')
    list_editable = ('is_hot',)
    list_display_links = ('id', 'title',)

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


admin.site.register(Post, PostAdmin)
