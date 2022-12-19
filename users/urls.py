from django.urls import path
from . import views

app_name = 'users'  # 定义一个命名空间  用于区分不同应用的连接地址

urlpatterns = [
    path('login.html', views.loginView, name='login')
]
