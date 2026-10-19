"""backend03 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from user.views import *

urlpatterns = [
    url(r'^login$', LoginAPIView.as_view()),  # 1.登录
    url(r'^register$', RegisterAPIView.as_view()),  # 2.注册
    # url(r'^verifyCode$', VerifyCodeAPIView.as_view()),  # 3.获取验证码
    # url(r'^forgetPassword$', ForgetPasswordAPIView.as_view()),  # 4.忘记密码
    # url(r'^studentConfirm$', StudentConfirmAPIView.as_view()),  # 5.学生认证
    url(r'^update$', UpdateAPIView.as_view()),  # 12.更新用户信息
    url(r'^getFriendList$', GetFriendListAPIView.as_view()),  # 14.获取好友列表
    url(r'^addFriend$', AddFriendAPIView.as_view()),  # 15.添加好友
    url(r'^responseAddFriend$', ResponseAddFriendAPIView.as_view()),  # 回应增加好友请求
    url(r'^deleteFriend$', DeleteFriendAPIView.as_view()),  # 16.删除好友
    url(r'^getUserInfo$', GetUserInfoAPIView.as_view()),  # 17.获取用户信息
    url(r'^survey$', SurveyAPIView.as_view()),  # 问卷
    url(r'^test$', TestAPIView.as_view()),
]
