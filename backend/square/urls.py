from django.conf.urls import url
from square.views import *

urlpatterns = [
    url(r'^getAllSquare$', GetAllSquareAPIView.as_view()),  # 18.获取全部广场信息
    url(r'^addSquare$', AddSquareAPIView.as_view()),  # 19.增加广场信息
]
