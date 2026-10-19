from rest_framework import exceptions
from user.models import UserToken
from rest_framework.authentication import BaseAuthentication
from datetime import datetime


class FirstAuthtication(BaseAuthentication):
    def authenticate(self, request):
        pass

    def authenticate_header(self, request):
        pass


class Authtication(BaseAuthentication):
    def authenticate(self, request):
        token = request.GET.get('token')
        token_obj = UserToken.objects.filter(token=token)  # get如果不存在会报错
        # print(token_obj)
        if not token_obj:
            raise exceptions.AuthenticationFailed(detail={'code': 201, 'detail': '用户未认证'})
        elif (datetime.now() - token_obj.create_time).total_seconds() <= 604800:  # 7天
            token_obj.delete()
            raise exceptions.AuthenticationFailed(detail={'code': 202, 'detail': '用户认证过期'})
        return (token_obj[0].user, token_obj[0])

    def authenticate_header(self, request):
        # 认证失败时给浏览器返回的响应头
        pass
