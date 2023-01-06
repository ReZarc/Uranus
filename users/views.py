from django.contrib import messages
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend  # 身份验证后端
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from .forms import LoginForm, RegisterForm, ForgetPwdForm, ModifyPwdForm, UserForm, UserProfileForm
from .models import EmailVerifyRecord, UserProfile
from django.core.mail import send_mail
import random
import string
from django.contrib.auth.decorators import login_required


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
        messages.error(request, '链接有误')
        return redirect('/')
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
                return redirect('/')
            else:
                messages.error(request, '帐号或密码错误')
                return redirect('users:login')
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
            messages.error(request, '注册成功')
            return redirect('/')
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
                messages.error(request, '邮件已经发送，请查收')
                return redirect('users:forget_pwd')
            else:
                messages.error(request, '邮箱未注册')
                return redirect('users:forget_pwd')
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
            messages.error(request, '修改成功')
            return redirect('/')
        else:
            messages.error(request, '修改失败')
            return redirect('users:forget_pwd_url')
    context = {'form': form}
    return render(request, 'users/modifypwd.html', context)


def modify_pwd(request):
    if request.method != 'POST':
        form = ModifyPwdForm()
    else:
        form = ModifyPwdForm(request.POST)
        if form.is_valid():
            if form.cleaned_data.get('password') == form.cleaned_data.get('password1'):
                user = User.objects.get(id=request.user.id)
                user.password = make_password(form.cleaned_data.get('password'))
                user.save()
                messages.error(request, '修改成功')
            else :
                messages.error(request, '两次密码不相同')
            return redirect('/')
        else:
            messages.error(request, '修改失败')
            return redirect('users:forget_pwd_url')
    context = {'form': form}
    return render(request, 'users/modifypwd.html', context)


def user_profile(request, user_id):
    user = User.objects.get(id=user_id)
    is_profile = len(UserProfile.objects.filter(owner_id=user_id))
    if is_profile:
        user_profile = UserProfile.objects.get(owner_id=user_id)
    else :
        user_profile = []
    context = {'user': user, 'user_profile': user_profile}
    return render(request, 'users/user_profile.html', context)


def logout_view(request):
    logout(request)
    return redirect('/')


@login_required(login_url='users:login')
def editor_users(request):
    """ 编辑用户信息 """
    user = User.objects.get(id=request.user.id)
    if request.method == "POST":
        try:
            userprofile = user.userprofile
            form = UserForm(request.POST, instance=user)   # 默认显示原有数据  保存加修改
            user_profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)  # 向表单填充默认数据
            # UserProfile与User 是一对一的关系，默认没有数据，注册成功后才会在个人中心设置信息
            # 第一次登录应当是空表单，如果设置了数据以后编辑时应当是修改，应该要默认显示所有的数据
            if form.is_valid() and user_profile_form.is_valid():
                form.save()
                user_profile_form.save()
                return redirect('users:user_profile')
        except UserProfile.DoesNotExist:   # 这里发生错误说明userprofile无数据
            form = UserForm(request.POST, instance=user)    # 默认显示原有数据  保存加修改
            user_profile_form = UserProfileForm(request.POST, request.FILES)  # 空表单，直接获取空表单的数据保存
            if form.is_valid() and user_profile_form.is_valid():
                form.save()
                # commit=False 先不保存，先把数据放在内存中，然后再重新给指定的字段赋值添加进去，提交保存新的数据
                new_user_profile = user_profile_form.save(commit=False)
                new_user_profile.owner = request.user
                new_user_profile.save()

                return redirect('users:user_profile')
    else:
        try:
            userprofile = user.userprofile
            form = UserForm(instance=user)
            user_profile_form = UserProfileForm(instance=userprofile)
        except UserProfile.DoesNotExist:
            form = UserForm(instance=user)
            user_profile_form = UserProfileForm()  # 显示空表单
    return render(request, 'users/editor_users.html', locals())
