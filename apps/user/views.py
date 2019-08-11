
from django.contrib.auth import login
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.views import View
from user.models import User
import re
import pysnooper

class RegisterView(View):
    # 返回注册页面
    @pysnooper.snoop()
    def get(self,request):
        return render(request, "register.html")

    @pysnooper.snoop()
    def post(self,request):
        user_name = request.POST.get("user_name")
        password = request.POST.get("pwd")
        cpassword = request.POST.get("cpwd")
        email = request.POST.get("email")
        allow = request.POST.get("allow")

        if not all([user_name,password,email]):
            return render(request,"register.html",{"errmsg":"数据不完整"})
        if password != cpassword:
            return render(request, "register.html", {"errmsg": "密码不一致"})
        if not allow:
            return render(request, "register.html", {"errmsg": "未勾选用户使用协议"})
        if not re.match('^.{8,20}$', password):
            return render(request, "register.html", {"errmsg": "密码不小于8位"})
        if re.match('^\W',user_name):
           return HttpResponseForbidden("用户名不能以特殊字符开头")
        if User.objects.filter(email=email).count() > 0:
            return render(request, "register.html", {"errmsg": "邮箱号已存在"})
        if User.objects.filter(username=user_name).count() > 0:
            return render(request, "register.html", {"errmsg": "用户名已存在"})
        try:
            user = User.objects.create_user(username=user_name, password=password, email=email)
            login(request, user)
            from django.urls import reverse
            return redirect(reverse("goods:index"))
        except:
            return render(request, "register.html", {"errmsg": "注册失败"})