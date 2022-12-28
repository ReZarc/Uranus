from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from djangoBlog.comment.forms import CommentForm
from djangoBlog.blog.models import Post


# Create your views here.
@login_required(login_url='users:login')
def comment(request, post_id, parent_comment_id=None):
    post = request.GET.get(Post, id=post_id)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        post = request.GET.get(Post, id=post_id)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.user = request.user
            new_comment.save()
            return redirect(post)
        else:
            return HttpResponse('内容有误，请重新填写')
    elif request.method == 'GET':
        comment_form = CommentForm()
        context = {
            'comment_form': comment_form,
            'post_id': post_id,
            'parent_comment_id': parent_comment_id
        }
        return render(request, 'blog/sidebar/comment.html', context)
