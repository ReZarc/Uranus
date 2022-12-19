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
    birth = models.DateField('生日', null=True, blank=True)
    gender = models.CharField('性别', max_length=6, choices=USER_GENDER_TYPE, default='male')     #选择框  默认 male
    image = models.ImageField(upload_to='images/%Y/%m', default='image/default.png', max_length=100, verbose_name='用户头像')   #存储目录, 默认头像, 最大长度, 默认值

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.owner.username
