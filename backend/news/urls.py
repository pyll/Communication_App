from django.conf.urls import url
from news.views import *

urlpatterns = [
    url(r'^getLike$', GetLikeAPIView.as_view()),  # 获取喜欢的信息
    url(r'^getFruit$', GetFruitAPIView.as_view()),  # 水果
    url(r'^getHotpot$', GetHotpotAPIView.as_view()),  # 火锅
    url(r'^getMilktea$', GetMilkteaAPIView.as_view()),  # 奶茶
    url(r'^getMeal$', GetMealAPIView.as_view()),  # 三餐
    url(r'^getBall$', GetBallAPIView.as_view()),  # 球类
    url(r'^getRun$', GetRunAPIView.as_view()),  # 跑步
    url(r'^getSwim$', GetSwimAPIView.as_view()),  # 游泳
    url(r'^getYoga$', GetYogaAPIView.as_view()),  # 瑜伽
    url(r'^getEnglish$', GetEnglishAPIView.as_view()),  # 英语
    url(r'^getHandwriting$', GetHandwritingAPIView.as_view()),  # 书法
    url(r'^getDraw$', GetDrawAPIView.as_view()),  # 绘画
    url(r'^getRead$', GetReadAPIView.as_view()),  # 读书
    url(r'^getSing$', GetSingAPIView.as_view()),  # 唱K
    url(r'^getFilm$', GetFilmAPIView.as_view()),  # 电影
    url(r'^getChess$', GetChessAPIView.as_view()),  # 下棋
    url(r'^getHomeparty$', GetHomepartyAPIView.as_view()),  # 轰趴
]
