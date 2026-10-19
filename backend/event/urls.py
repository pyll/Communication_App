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
# from django.contrib import admin
from django.conf.urls import url
from event.views import *

urlpatterns = [
    url(r'^getAllEvent$', GetAllEventAPIView.as_view()),  # 6.获取动态信息
    url(r'^getFoodEvent$', GetFoodEventAPIView.as_view()),  # 7.获取食的动态信息
    url(r'^getSportEvent$', GetSportEventAPIView.as_view()),  # 8.获取行的动态信息
    url(r'^getStudyEvent$', GetStudyEventAPIView.as_view()),  # 9.获取学的动态信息
    url(r'^getPlayEvent$', GetPlayEventAPIView.as_view()),  # 10.获取乐的动态信息
    url(r'^addEvent$', AddEventAPIView.as_view()),  # 11.用户发布动态
    url(r'^getMyEvent$', GetMyEventAPIView.as_view()),  # 16.获取我的动态
    url(r'^delMyEvent$', DelMyEventAPIView.as_view()),  # 17.删除我的动态
]
