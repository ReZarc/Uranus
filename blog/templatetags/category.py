# 在这里自定义模板标签
# https://docs.djangoproject.com/zh-hans/3.2/howto/custom-template-tags/  官方文档
from django import template
from blog.models import Category, Sidebar, Post, Comment
from users.models import User
register = template.Library()


@register.simple_tag
def get_category_list():
    # 全站的分类
    return Category.objects.all()


@register.simple_tag
def get_sidebar_list():
    # 侧边栏
    return Sidebar.get_sidebar()


@register.simple_tag
def get_new_post():
    # 最新文章
    return Post.objects.order_by('-add_date')[:5]


@register.simple_tag
def get_hot_post():
    # 手动热门推荐
    return Post.objects.filter(is_hot=True)[:3]


@register.simple_tag
def get_hot_pv_post():
    # 手动热门推荐
    return Post.objects.filter(is_hot=False).order_by('-pv')[:5 - min(3, len(Post.objects.filter(is_hot=True)))]


@register.simple_tag
def get_archives():
    # 文章归档
    return Post.objects.dates('add_date', 'month', order='DESC')[:5]


@register.simple_tag
def get_comments():

    return Comment.objects.order_by('-created')[:3]