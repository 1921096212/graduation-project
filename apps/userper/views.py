import json

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from . import models


def logins(request):
    if request.method == "POST":
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user_obj = authenticate(username=username, password=password)
        if user_obj:
            login(request, user_obj)
            return redirect('/')  # 登录成功,重定向到主页
        else:
            message = "密码不正确！"
        return render(request, 'user/login.html', {"message": message})
    return render(request, 'user/login.html')


def register(request):
    if request.method == "POST":
        name = request.POST.get('name', None)
        password = request.POST.get('password', None)
        grade = request.POST.get('grade', None)
        number = request.POST.get('number', None)
        try:
            user = User.objects.create_user(username=number, password=password)
            models.Contact.objects.create(grade=grade, name=name, user_id=user.id)
        except IntegrityError:
            messages.error(request, '该用户已注册!')
            return redirect('/register')
        return redirect('/login')  # 注册成功,重定向到login
    return render(request, 'user/register.html')


def logout_view(request):
    logout(request)
    return redirect('/')


# 修改用户资料
@login_required
@csrf_exempt
def change_data(request):
    user = request.user  # 获取用户名
    msg = None
    # # 修改名字
    if request.method == 'PUT':
        dict_data = json.loads(request.body.decode('utf8'))
        new_username = dict_data.get('username').strip()
        if not new_username:
            msg = "名字不能为空"
            return JsonResponse({"msg": msg})
        # 这里的查询不恰当
        obj = models.Contact.objects.filter(user_id=request.user.id)[0]
        obj.name = new_username
        obj.save()
        msg = "修改成功"
        return JsonResponse({"msg": msg})

    # 修改密码
    if request.method == 'POST':
        old_password = request.POST.get("old_password", "")  # 获取原来的密码，默认为空字符串
        new_password = request.POST.get("new_password", "")  # 获取新密码，默认为空字符串

        if not old_password and not new_password:
            messages.error(request, '密码不能为空!')
            return redirect('/change')

        if user.check_password(old_password):  # 到数据库中验证旧密码通过
            user.set_password(new_password)  # 修改密码
            user.save()
            return redirect("/")
        else:
            messages.error(request, '旧密码输入错误!')
            return redirect('/change')
    u = models.Contact.objects.filter(user_id=request.user.id).only('name')
    return render(request, "user/change.html", locals())
