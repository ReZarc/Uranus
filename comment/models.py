from django.db import models
import uuid
from ckeditor.fields import RichTextField
from mptt.models import MPTTModel, TreeForeignKey
from djangoBlog.blog.models import Post
from djangoBlog.users.models import User


# Create your models here.
class Comment(models.Model):  # 博文评论
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    body = RichTextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)
        verbose_name_plural = '评论'

    def __str__(self):
        return self.body[:20]