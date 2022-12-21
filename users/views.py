from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend  # 身份验证后端
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from .forms import LoginForm, RegisterForm, ForgetPwdForm, ModifyPwdForm
from .models import EmailVerifyRecord
from django.core.mail import send_mail
import random
import string


class MyBackend(ModelBackend):
    # 邮箱登录注册
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):  # 加密明文密码
                return user
        except Exception as e:
            return None


def active_user(request, active_code):
    # 比对验证码
    all_records = EmailVerifyRecord.objects.filter(code=active_code)
    if all_records:
        for it in all_records:
            email = it.email
            user = User.objects.get(email=email)
            user.is_staff = True
            user.save()
    else:
        return HttpResponse('链接有误')
    return redirect('users:login')


# Create your views here.
def loginView(request):
    if request.method != 'POST':  # 是否 POST 格式
        form = LoginForm()  # 空表单
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']  # 获取帐号
            password = form.cleaned_data['password']  # 获取密码
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/admin')
            else:
                return HttpResponse('帐号或密码错误')
    context = {'form': form}
    return render(request, 'users/login.html', context)


def random_str(length=6):
    # 生成随机字符串
    chars = string.ascii_letters + string.digits
    code = ''.join(random.sample(chars, length))
    return code


def send_register_email(email, send_type='register'):
    email_record = EmailVerifyRecord()
    code = random_str()
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    # email_record.add_time = datetime.now()
    email_record.save()

    if send_type == 'register':
        email_title = '博客的注册激活链接'
        email_body = '请点击以下链接激活账号：http://127.0.0.1:8000/users/active/{0}'.format(code)

        send_status = send_mail(email_title, email_body, 'rezarc@qq.com', [email])
        if send_status:
            pass

    elif send_type == 'forget':
        email_title = '找回密码链接'
        email_body = '请点击以下链接修改密码：http://127.0.0.1:8000/users/forget_pwd_url/{0}'.format(code)

        send_status = send_mail(email_title, email_body, 'rezarc@qq.com', [email])
        if send_status:
            pass


# 注册页面
def register(request):
    if request.method != 'POST':
        form = RegisterForm()
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data.get('password'))
            # new_user.username = form.cleaned_data.get('email')
            new_user.save()
            send_register_email(form.cleaned_data.get('email'), 'register')
            return HttpResponse('注册成功')
    context = {'form': form}
    return render(request, 'users/register.html', context)


def forget_pwd(request):
    if request.method == 'GET':
        form = ForgetPwdForm()
    elif request.method == 'POST':
        form = ForgetPwdForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            exists = User.objects.filter(email=email).exists()
            if exists:
                send_register_email(email, 'forget')
                return HttpResponse('邮件已经发送，请查收')
            else:
                return HttpResponse('邮箱未注册')
    context = {'form': form}
    return render(request, 'users/forget_pwd.html', context)


def forget_pwd_url(request, active_code):
    if request.method != 'POST':
        form = ModifyPwdForm()
    else:
        form = ModifyPwdForm(request.POST)
        if form.is_valid():
            record = EmailVerifyRecord.objects.get(code=active_code)
            email = record.email
            user = User.objects.get(email=email)
            user.password = make_password(form.cleaned_data.get('password'))
            user.save()
            return HttpResponse('修改成功')
        else:
            return HttpResponse('修改失败')
    context = {'form': form}
    return render(request, 'users/modifypwd.html', context)