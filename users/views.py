from django.shortcuts import render,HttpResponse
from django.contrib.auth import authenticate, login
# Create your views here.
def loginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')     # 获取帐号
        password = request.POST.get('password')     # 获取密码
        # print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse('登录成功')
        else:
            return HttpResponse('登录失败')

    return render(request, 'users/login.html')
