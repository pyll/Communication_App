from django.conf.urls import url
from talk.views import *

urlpatterns = [
    url(r'websocketLink/(?P<roomname>\w+)', websocketLink),  # webSocket 链接
    # url(r'websocketLink', websocketLink),  # webSocket 链接
]
