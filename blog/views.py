from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, F
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import CommentForm, PostForm
from .models import Post, Comment, Favorite, Category, Post
from users.models import User


def index(request):
    # 首页
    post_list = Post.objects.all()  # 查询到所有的文章,queryset
    # 分页方法
    paginator = Paginator(post_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, 'blog/index.html', context)


def category_list(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    # 获取当前分类下的所有文章
    posts = category.post_set.all()
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'category': category, 'page_obj': page_obj}
    return render(request, 'blog/list.html', context)


def my_post_list(request):
    posts = Post.objects.filter(owner_id=request.user.id)
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, 'blog/my_post.html', context)


def post_detail(request, post_id):
    # 文章详情页
    post = get_object_or_404(Post, id=post_id)

    # 用文章id来实现的上下篇
    prev_post = Post.objects.filter(id__lt=post_id).last()  # 上一篇
    next_post = Post.objects.filter(id__gt=post_id).first()  # 下一篇
    Post.objects.filter(id=post_id).update(pv=F('pv') + 1)  # 浏览
    comments = Comment.objects.filter(post_id=post_id)
    comment_form = CommentForm()
    is_favorite = len(Favorite.objects.filter(user_id=request.user.id, post_id=post_id))

    # 用发布日期来实现上下篇
    # date_prev_post = Post.objects.filter(add_date__lt=post.add_date).last()
    # date_next_post = Post.objects.filter(add_date__gt=post.add_date).first()
    context = {
        'post': post,
        'prev_post': prev_post,
        'next_post': next_post,
        'comments': comments,
        'comment_form': comment_form,
        'is_favorite': is_favorite
    }
    return render(request, 'blog/detail.html', context)


def search(request):
    """ 搜索视图 """
    keyword = request.GET.get('keyword')
    # 没有搜索默认显示所有文章
    if not keyword:
        post_list = Post.objects.all()
    else:
        # 包含查询的方法，用Q对象来组合复杂查询
        post_list = Post.objects.filter(
            Q(title__icontains=keyword) | Q(desc__icontains=keyword) | Q(content__icontains=keyword))
    paginator = Paginator(post_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    return render(request, 'blog/index.html', context)


def archives(request, year, month):
    # 文章归档列表页
    post_list = Post.objects.filter(add_date__year=year, add_date__month=month)
    paginator = Paginator(post_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj, 'year': year, 'month': month}
    return render(request, 'blog/archives_list.html', context)


@login_required(login_url='users:login')
def post_comment(request, post_id, parent_comment_id=None):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        post = Post.objects.get(id=post_id)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.user = request.user
            new_comment.save()
            return redirect('blog:post_detail', post_id)
        else:
            return HttpResponse('内容有误，请重新填写')
    else:
        form = CommentForm()

    context = {
        'form': form,
        'post_id': post_id,
        'parent_comment_id': parent_comment_id
    }
    return render(request, 'blog/detail.html', context)


@login_required(login_url='users:login')
def post_release(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.owner = request.user
            new_post.save()
            post_id = new_post.id
            return redirect('blog:post_detail', post_id)
    else:
        form = PostForm()
    context = {'form': form}
    return render(request, 'blog/release.html', context)


@login_required(login_url='users:login')
def post_edit(request, post_id):
    user_id = Post.objects.get(id=post_id).owner_id
    if user_id != request.user.id:
        messages.error(request, '没有编辑权限！')
        return redirect('blog:post_detail', post_id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            Post.objects.filter(id=post_id).update(
                title=post.title,
                desc=post.desc,
                category_id=post.category.id,
                content=post.content
            )
            return redirect('blog:post_detail', post_id)
    else:
        form = PostForm()
    context = {'form': form, 'user_id': user_id}
    return render(request, 'blog/edit.html', context)


@login_required(login_url='users:login')
def post_delete(request, post_id):
    user = Post.objects.get(id=post_id).owner_id
    if request.user.id == user:
        Post.objects.filter(id=post_id).delete()
    return redirect('/')


@login_required(login_url='users:login')
def comment_delete(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    post_id = comment.post_id
    Comment.objects.filter(id=comment_id).delete()
    return redirect('blog:post_detail', post_id)


# def comment_sidebar(request):
#     comment = Comment.objects.all()
#     return render(request, 'blog/sidebar/comment.html')
@login_required(login_url='users:login')
def favorite_add(request, post_id):
    user = request.user.id
    post = post_id
    Favorite.objects.create(user_id=user, post_id=post)
    return redirect('blog:post_detail', post_id)


@login_required(login_url='users:login')
def favorite_del(request, post_id):
    user = request.user.id
    post = post_id
    Favorite.objects.filter(user_id=user, post_id=post).delete()
    return redirect('blog:post_detail', post_id)


# @login_required(login_url='users:login')
def my_favorite(request):
    post = Favorite.objects.filter(user_id=request.user.id).values('post_id')
    posts = []
    for it in post:
        posts += Post.objects.filter(id=it['post_id'])
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, 'blog/my_favorite.html', context)


def post_list(request, user_id):
    user = User.objects.get(id=user_id)
    posts = Post.objects.filter(owner_id=user_id)
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj, 'user': user}
    return render(request, 'blog/post_list.html', context)
