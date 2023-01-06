from django import forms
from django.contrib.auth.models import User

from .models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=35, widget=forms.TextInput(attrs={
        'class': 'input', 'placeholder': '用户名/邮箱'
    }))
    password = forms.CharField(label='密码', min_length=6, widget=forms.PasswordInput(attrs={
        'class': 'input', 'placeholder': '密码'
    }))

    # 验证密码
    def clean_password(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username == password:
            raise forms.ValidationError('用户名与密码不能相同')
        return password


# 注册表单
class RegisterForm(forms.ModelForm):
    username = forms.CharField(label='用户名', max_length=35, widget=forms.TextInput(attrs={
        'class': 'input', 'placeholder': '用户名'
    }))
    email = forms.EmailField(label='邮箱', max_length=35, widget=forms.EmailInput(attrs={
        'class': 'input', 'placeholder': '邮箱'
    }))
    password = forms.CharField(label='密码', min_length=6, widget=forms.PasswordInput(attrs={
        'class': 'input', 'placeholder': '密码'
    }))
    password1 = forms.CharField(label='再次输入密码', min_length=6, widget=forms.PasswordInput(attrs={
        'class': 'input', 'placeholder': '再次输入密码'
    }))

    class Meta:
        model = User
        # fields = ('username', 'password')
        fields = ('username', 'email', 'password')

    # 验证用户名是否存在
    def clean_username(self):
        username = self.cleaned_data.get('username')
        exists = User.objects.filter(username=username).exists()
        if exists:
            raise forms.ValidationError('用户名已存在')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        exists = User.objects.filter(email=email).exists()
        if exists:
            raise forms.ValidationError('邮箱已注册')
        return email

    # 验证密码是否相等
    def clean_password1(self):
        if self.cleaned_data['password'] != self.cleaned_data['password1']:
            raise forms.ValidationError('两次密码输入不一致')
        return self.cleaned_data['password1']


# 忘记密码
class ForgetPwdForm(forms.Form):
    email = forms.EmailField(label='邮箱', max_length=35, widget=forms.EmailInput(attrs={
        'class': 'input', 'placeholder': '邮箱'
    }))


# 修改密码
class ModifyPwdForm(forms.Form):
    password = forms.CharField(label='输入新密码', min_length=6, widget=forms.PasswordInput(attrs={
        'class': 'input', 'placeholder': '密码'
    }))
    password1 = forms.CharField(label='再次输入密码', min_length=6, widget=forms.PasswordInput(attrs={
        'class': 'input', 'placeholder': '再次输入密码'
    }))


class UserForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'input'
    }))
    birth = forms.DateField(widget=forms.DateInput(attrs={
        'class': 'input'
    }))

    class Meta:
        model = User
        fields = ('email',)


# 编辑个人信息表单
class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('nickName', 'desc', 'birth', 'gender', 'image')
