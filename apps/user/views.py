import re
from django.conf import settings
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse
from django import http
from django.views import View
from celery_tasks.email.tasks import send_sms
from user.models import User
from utils import verify_token
import pysnooper

@pysnooper.snoop()
def generate_verify_email_url(user):
    token = verify_token.dumps(user)
    verify_url = settings.EMAIL_VERIFY_URL + "?token=" + token
    return verify_url


class RegisterView(View):
    # 返回注册页面

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
            user.is_active = 0
            # 发送激活邮件
            verify_url = generate_verify_email_url(user)
            send_sms.delay(email, verify_url)
            user.save()
            return redirect(reverse("goods:index"))
        except:
            return render(request, "register.html", {"errmsg": "注册失败"})


class EmailActiveView(View):
    @pysnooper.snoop()
    def get(self,request):
        token = request.GET.get("token")
        if not token:
            return http.HttpResponseBadRequest("缺少token")
        data = verify_token.loads(token)
        if not data:
            return http.HttpResponseForbidden("无效的token")
        try:
            User.objects.filter(id=data["user_id"]).update(is_active=1)
        except:
            return http.HttpResponseServerError("激活邮件失败")
        # return redirect(reverse("goods:index"))
        return http.HttpResponse("邮箱激活成功")