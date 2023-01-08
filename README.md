# 基于Django的在线博客管理系统
这是一个基于 Django 框架的博客论坛网站搭建。
## 环境搭建
Python: 3.10

Django: 4.1.4

Dominate-Layui: 2020.6.25post1

Pillow: 9.3.0

asgiref: 3.5.2

cmdlet: 0.4.2

Django-ckeditor: 6.5.1

Django-email-users: 1.1.0

Django-js-asset: 2.0.0

Django-mptt: 0.14.0

SQLite

settings.py、users/views.send_register_email中服务器邮箱和密码请修改，否则在通过服务器发送邮件后会报错。

## 实现功能：

### 用户相关

登录注册

修改密码

忘记密码

邮箱激活

个人主页

### 博客相关

发布修改

收藏删除

发布评论

评论删除

通过ckeditor渲染
