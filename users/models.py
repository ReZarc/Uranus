from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserProfile(models.Model):
    USER_GENDER_TYPE = (
        ('male', '男'),
        ('female', '女'),
    )
    owner = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户')  # 一对一扩展
    nickName = models.CharField('昵称', max_length=50, default='')
    desc = models.CharField('个人简介', max_length=200, blank=True, default='这个人很懒，什么都没有写。') # 个人简介
    birth = models.DateField('生日', null=True, blank=True)
    gender = models.CharField('性别', max_length=6, choices=USER_GENDER_TYPE, default='male')     #选择框  默认 male
    image = models.ImageField(upload_to='images/%Y/%m', default='images/default.png', max_length=100, verbose_name='用户头像')   #存储目录, 默认头像, 最大长度, 默认值

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.owner.username


class EmailVerifyRecord(models.Model):
    SEND_TYPE_CHOICES = (
        ('register', '注册'),
        ('forget', '找回密码')
    )
    code = models.CharField('验证码', max_length=6)
    email = models.EmailField('邮箱', max_length=35)
    send_type = models.CharField(choices=SEND_TYPE_CHOICES, default='register', max_length=25)

    class Meta:
        verbose_name = '验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code


